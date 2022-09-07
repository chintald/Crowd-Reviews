import graphene
from django.contrib.auth import get_user_model

from api.account.types import User

UserModel = get_user_model()


class AccountQueries(graphene.ObjectType):
    all_users = graphene.List(User, description="Return the currently authenticated user.")

    # @login_required
    def resolve_all_users(self, info):
        qs = UserModel.objects.all()
        print(qs)
        return qs

        # user = info.context.user
        # if user.like_time is None:
        #     user.user_like_time()
        # return user