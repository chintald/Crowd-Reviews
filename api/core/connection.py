import graphene
from graphene_django import DjangoObjectType
from graphene.relay.connection import Connection


class NonNullConnection(Connection):
    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, node=None, name=None, **options):
        super().__init_subclass_with_meta__(node=node, name=name, **options)

        # Override the original EdgeBase type to make to `node` field required.
        class EdgeBase:
            node = graphene.Field(
                cls._meta.node,
                description="The item at the end of the edge.",
                required=True,
            )
            cursor = graphene.String(
                required=True, description="A cursor for use in pagination."
            )

        # Create the edge type using the new EdgeBase.
        edge_name = cls.Edge._meta.name
        edge_bases = (EdgeBase, graphene.ObjectType)
        edge = type(edge_name, edge_bases, {})
        cls.Edge = edge

        # Override the `edges` field to make it non-null list
        # of non-null edges.
        cls._meta.fields["edges"] = graphene.Field(
            graphene.NonNull(graphene.List(graphene.NonNull(cls.Edge)))
        )


class CountableConnection(NonNullConnection):
    class Meta:
        abstract = True

    total_count = graphene.Int(description="A total count of items in the collection.")

    @staticmethod
    def resolve_total_count(root, *_args, **_kwargs):
        if isinstance(root.iterable, list):
            return len(root.iterable)
        return root.iterable.count()


class CountableDjangoObjectType(DjangoObjectType):
    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, *args, **kwargs):
        # Force it to use the countable connection
        countable_conn = CountableConnection.create_type(
            "{}CountableConnection".format(cls.__name__), node=cls
        )
        super().__init_subclass_with_meta__(*args, connection=countable_conn, **kwargs)
