import graphene


class BookmarkInputType(graphene.InputObjectType):
    url = graphene.NonNull(graphene.String)