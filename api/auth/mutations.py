import graphene
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from django.utils.crypto import get_random_string

from api.account.types import User
from api.auth.exceptions import UserAccount
from api.auth.inputs import LoginInput, SigninInput
from api.jwt import create_access_token

UserModel = get_user_model()


class UserSignupMutation(graphene.Mutation):
    success = graphene.Boolean(default_value=False)
    user = graphene.Field(User)

    class Arguments:
        input = SigninInput(description="Fields required to ")

    @classmethod
    def mutate(cls, root, info, input):
        success = False
        user = None
        credentials_valid = cls.check_user_credentials(input)
        if credentials_valid:
            create_user = UserModel(email=input.email, username=input.username)
            create_user.set_password(input.password)
            incorrect_password = validate_password(password=input.password, user=create_user)
            create_user.save()
            success = True
            user = create_user
        return UserSignupMutation(success=success, user=user)

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
    user = graphene.Field(User)
    access_token = graphene.String()

    class Arguments:
        input = LoginInput(description="Fields required to login to your account", required=True)

    @classmethod
    def mutate(cls, root, info, input):
        access_token = None
        user = None
        success = False
        email_or_username = input.email_or_username
        user_obj_query = UserModel.objects.filter(Q(email=email_or_username) | Q(username=email_or_username))
        user_obj = cls.check_login_credentials(user_obj_query, input.password)
        if user_obj:
            access_token = create_access_token(user_obj)
            success = True
            user = user_obj
        return UserLoginMutation(success=success, user=user, access_token=access_token)

    @classmethod
    def check_login_credentials(cls, user_query, password):
        if user_query.count() == 1:
            user_obj = user_query.first()
            is_password_valid = user_obj.check_password(password)
            if not is_password_valid:
                raise UserAccount.CredentialsNotValid()
            user_obj.jwt_token_key = get_random_string()
            user_obj.save()
        elif not user_query:
            raise UserAccount.UserDoesNotExist()
        else:
            raise UserAccount.ServerError()
        return user_obj
