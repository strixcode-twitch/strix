import graphene


class FolderInputType(graphene.InputObjectType):
    name = graphene.NonNull(graphene.String)
    parent_id = graphene.NonNull(graphene.ID)