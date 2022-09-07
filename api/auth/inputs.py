import graphene


class LoginInput(graphene.InputObjectType):
    email = graphene.String(description="Email of the user", required=True)


class SigninInput(graphene.InputObjectType):
    email = graphene.String(description="Email of the user", required=True)
    password = graphene.String(description="Password of the user", required=True)
    confirm_password = graphene.String(description="Confirm password", required=True)
