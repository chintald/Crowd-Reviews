import graphene
from django.contrib.auth import get_user_model

from api.core.connection import CountableDjangoObjectType


class User(CountableDjangoObjectType):
    email = graphene.String()

    class Meta:
        description="Represents User Node"
        interfaces = [graphene.relay.Node, ]
        model = get_user_model()

    @classmethod
    def resolve_email(cls, root, info):
        return f"{root.email}"
