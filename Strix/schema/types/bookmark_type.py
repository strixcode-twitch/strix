import graphene


class BookmarkType(graphene.ObjectType):
    class Meta:
        name = 'Bookmark'
        interfaces = (graphene.relay.Node,)

    title = graphene.String()
    url = graphene.String()
    description = graphene.String()
    icon = graphene.String()

    @classmethod
    def get_node(cls, info, uid):
        return BookmarkType(uid=uid, title="Title", url="url", description="description", icon="icon")


class BookmarkTypeConnection(graphene.relay.Connection):
    class Meta:
        name = 'BookmarkConnection'
        node = BookmarkType
