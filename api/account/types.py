import graphene
from django.contrib.auth import get_user_model

from api.core.connection import CountableDjangoObjectType
from api.jwt import create_access_token


class User(CountableDjangoObjectType):
    email = graphene.String()
    access_token = graphene.String()

    class Meta:
        description = "Represents User Node"
        interfaces = [graphene.relay.Node, ]
        model = get_user_model()

    @classmethod
    def resolve_email(cls, root, info):
        return f"{root.email}"

    @classmethod
    def resolve_access_token(cls, root, info):
        return create_access_token(root)
