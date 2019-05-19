import graphene

from Strix.schema.resolvers.bookmark_resolvers import resolve_bookmarks, CreateBookmark
from Strix.schema.resolvers.tag_resolver import CreateTag
from Strix.schema.resolvers.user_resolvers import resolve_user
from Strix.schema.types.bookmark_type import BookmarkTypeConnection
from Strix.schema.types.folder_type import FolderType
from Strix.schema.types.user_type import UserType
from Strix.services.user_service import get_current_user

def resolve_root_folder(self, info: graphene.ResolveInfo, **args):
    return None

class Me(graphene.ObjectType):
    """ My objects """

    class Meta:
        interfaces = (graphene.relay.Node,)

    first_name = graphene.String()
    last_name = graphene.String()
    full_name = graphene.String()
    email = graphene.String()

    bookmarks = graphene.relay.ConnectionField(
        BookmarkTypeConnection, description='Your bookmarks!', resolver=resolve_bookmarks
    )

    root_folder = graphene.Field(FolderType)

    def resolve_full_name(root, info, **args):
        return '{} {}'.format(root.first_name, root.last_name)

    @classmethod
    def get_node(cls, info, id):
        return None


class Query(graphene.ObjectType):
    user = graphene.Field(lambda: UserType, resolver=resolve_user)

    me = graphene.Field(Me)
    node = graphene.relay.Node.Field()

    def resolve_me(self, info, **args):
        user = get_current_user(args.get('user_id'))
        return Me(**user.get_gql_node())


class Mutation(graphene.ObjectType):
    create_bookmark = CreateBookmark.Field()
    create_tag = CreateTag.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)



