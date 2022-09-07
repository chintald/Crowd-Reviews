import graphene
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from api.account.types import User
from api.auth.exceptions import UserCredentials
from api.auth.inputs import LoginInput, SigninInput


UserModel = get_user_model()


class UserSignupMutation(graphene.Mutation):
    success = graphene.Boolean(default_value=False)
    data = graphene.Field(User)
    error_message = graphene.String()

    class Arguments:
        input = SigninInput(description="Fields required to ")

    @classmethod
    def mutate(cls, root, info, input):
        success = False
        data = None
        is_new_user, error_message = cls.check_user(input)
        if is_new_user:
            create_user = UserModel(email=input.email, password=input.password)
            create_user.save()
            success = True
            data = create_user

        return UserSignupMutation(success=success, error_message=error_message, data=data)




    @classmethod
    def check_user(cls, input):
        is_new_user = False
        error_message = None

        password = input.password
        confirm_password = input.confirm_password
        email = input.email

        if password != confirm_password:
            error_message = UserCredentials().credentials_not_valid()

        try:
            user_obj = UserModel.objects.get(email=email)
            if user_obj:
                error_message = UserCredentials().user_already_exist()
        except UserModel.DoesNotExist:
            is_new_user = True

        return is_new_user, error_message







class UserLoginMutation(graphene.Mutation):
    error_message = graphene.String()
    success = graphene.Boolean()
    data = graphene.Field(User)

    class Arguments:
        input = LoginInput(description="Fields required to login to your account", required=True)

    @classmethod
    def mutate(cls, root, info, input):
        email = input.email
        try:
            user_obj = UserModel.objects.get(email=email)
            user_obj.jwt_token_key = get_random_string()
            user_obj.save()

            success = True
            data = user_obj
            error_message = None

        except UserModel.DoesNotExist:
            success = False
            error_message = "Please check the credentials."
            data = None

        return UserLoginMutation(success=success, data=data, error_message=error_message)
