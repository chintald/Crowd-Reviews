import graphene
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required

from api.account.types import User

UserModel = get_user_model()


class AccountQueries(graphene.ObjectType):
    current_user = graphene.Field(User, description="Return the currently authenticated user.")

    @login_required
    def resolve_current_user(self, info):
        user_obj = UserModel.objects.get(pk=info.context.user.id)
        return user_obj

        # user = info.context.user
        # if user.like_time is None:
        #     user.user_like_time()
        # return user