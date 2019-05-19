import graphene


class TagType(graphene.ObjectType):
    class Meta:
        name = 'Tag'
        interfaces = (graphene.relay.Node,)

    name = graphene.String()


class TagTypeConnection(graphene.relay.Connection):
    class Meta:
        name = 'TagConnection'
        node = TagType
