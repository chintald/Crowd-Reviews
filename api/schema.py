import graphene

from graphql_auth.schema import UserQuery, MeQuery

from api.account.schema import AccountQueries
from api.auth.schema import AuthMutations


class Query(AccountQueries):
    pass


class Mutation(AuthMutations):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

