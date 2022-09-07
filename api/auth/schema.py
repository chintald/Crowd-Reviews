import graphene

from api.auth.mutations import UserLoginMutation, UserSignupMutation


class AuthMutations(graphene.ObjectType):
    user_login = UserLoginMutation.Field()
    user_signup = UserSignupMutation.Field()
