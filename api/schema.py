import graphene

from graphql_auth.schema import UserQuery, MeQuery

from api.account.schema import AccountQueries


class Query(AccountQueries):
    pass


schema = graphene.Schema(query=Query)
