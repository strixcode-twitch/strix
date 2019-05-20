import graphene

from Strix.models.folder import Folder
from Strix.schema.input_types.folder_input_type import FolderInputType
from Strix.schema.types.folder_type import FolderType
from Strix.services.folder_service import folder_get_root, create_sub_folder, get_folder
from Strix.services.user_service import get_current_user


def resolve_root_folder(self, info: graphene.ResolveInfo, **args) -> FolderType:
    folder = folder_get_root(args.get('user_id'))
    return FolderType(**folder.get_gql_node())


def resolve_folder(self, info: graphene.ResolveInfo, **args):
    folder = get_folder(args.get('user_id'), args.get('folder_id'))
    return FolderType(**folder.get_gql_node())


class CreateFolder(graphene.Mutation):
    class Arguments:
        folder = FolderInputType(required=True)

    Output = FolderType

    def mutate(self, info: graphene.ResolveInfo, folder: FolderInputType, **args):
        entity = create_sub_folder(args.get('user_id'), folder.parent_id, folder.name)
        return FolderType(**entity.get_gql_node())
