import graphene
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from django.utils.crypto import get_random_string

from api.account.types import User
from api.auth.exceptions import UserAccount
from api.auth.inputs import LoginInput, SigninInput


UserModel = get_user_model()


class UserSignupMutation(graphene.Mutation):
    success = graphene.Boolean(default_value=False)
    data = graphene.Field(User)

    class Arguments:
        input = SigninInput(description="Fields required to ")

    @classmethod
    def mutate(cls, root, info, input):
        success = False
        data = None
        credentials_valid = cls.check_user_credentials(input)
        if credentials_valid:
            create_user = UserModel(email=input.email, username=input.username)
            create_user.set_password(input.password)
            incorrect_password = validate_password(password=input.password, user=create_user)

            create_user.save()
            success = True
            data = create_user
        return UserSignupMutation(success=success, data=data)

    @classmethod
    def check_user_credentials(cls, input):
        credentials_valid = False

        password = input.password
        confirm_password = input.confirm_password
        email = input.email
        username = input.username

        if password != confirm_password:
            raise UserAccount().CredentialsNotValid()

        user_query = UserModel.objects.filter(username=username)
        if user_query.count() > 0:
            check_same_user = user_query.filter(email=input.email).count()
            if check_same_user > 0:
                raise UserAccount().UserAlreadyExist()
            raise UserAccount().UsernameExist()

        try:
            user_obj = UserModel.objects.get(email=email)
            if user_obj:
                raise UserAccount().UserAlreadyExist()
        except UserModel.DoesNotExist:
            credentials_valid = True

        return credentials_valid


class UserLoginMutation(graphene.Mutation):
    success = graphene.Boolean()
    data = graphene.Field(User)

    class Arguments:
        input = LoginInput(description="Fields required to login to your account", required=True)

    @classmethod
    def mutate(cls, root, info, input):
        email_or_username = input.email
        try:
            user_obj_query = UserModel.objects.filter(Q(email=email_or_username) | Q(username=email_or_username))
            if user_obj_query.count() == 1:
                is_password_valid = user_obj_query.first().check_password(input.password)
                if not is_password_valid:
                    raise UserAccount.CredentialsNotValid()
            # user_obj.jwt_token_key = get_random_string()
            # user_obj.save()

            success = True
            data = user_obj_query

        except UserModel.DoesNotExist:
            success = False
            error_message = UserAccount().CredentialsNotValid()
            data = None

        return UserLoginMutation(success=success, data=data)
