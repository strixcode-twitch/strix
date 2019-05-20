import graphene

from Strix.models.folder import Folder


def resolve_subfolders(self, info: graphene.ResolveInfo, **args):
    parent: Folder = Folder.nodes.get_or_none(uid=self.id)

    return [FolderType(**x.get_gql_node()) for x in parent.children]


class FolderType(graphene.ObjectType):
    class Meta:
        name = 'Folder'
        interfaces = (graphene.relay.Node, )

    name = graphene.String()
    folders = graphene.relay.ConnectionField(
        'Strix.schema.types.folder_type.FolderTypeConnection', description="Sub folders", resolver=resolve_subfolders
    )


class FolderTypeConnection(graphene.relay.Connection):
    class Meta:
        name = 'FolderConnection'
        node = FolderType
