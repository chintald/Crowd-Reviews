import graphene
from django.contrib.auth import get_user_model
from graphql_auth.schema import UserNode


UserModel = get_user_model()


class AccountQueries(graphene.ObjectType):
    all_users = graphene.Field(UserNode, description="Return the currently authenticated user.")

    # @login_required
    def resolve_all_users(self, info):
        qs = UserModel.objects.create(email="chintaldraval@gmail.com")
        print(qs)
        # return qs

        # user = info.context.user
        # if user.like_time is None:
        #     user.user_like_time()
        # return user