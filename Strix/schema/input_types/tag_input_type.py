import graphene


class TagInputType(graphene.InputObjectType):
    name = graphene.NonNull(graphene.String)
    bookmark_id = graphene.NonNull(graphene.ID)