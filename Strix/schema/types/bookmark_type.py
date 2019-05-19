import graphene
from graphql import ResolveInfo

from Strix.schema.types.tag_type import TagTypeConnection
from Strix.services.bookmark_service import get_bookmark
from Strix.services.tag_service import get_bookmark_tags
from Strix.services.user_service import get_current_user


def resolve_bookmark_tags(self, info: ResolveInfo, **args):
    user = get_current_user(args.get('user_id'))
    bookmark = get_bookmark(self.id)
    tags = get_bookmark_tags(bookmark, user)
    return tags


class BookmarkType(graphene.ObjectType):
    class Meta:
        name = 'Bookmark'
        interfaces = (graphene.relay.Node,)

    title = graphene.String()
    url = graphene.String()
    description = graphene.String()
    icon = graphene.String()

    tags = graphene.relay.ConnectionField(
        TagTypeConnection, description='Tags applied to this bookmark', resolver=resolve_bookmark_tags
    )

    @classmethod
    def get_node(cls, info, uid):
        return BookmarkType(uid=uid, title="Title", url="url", description="description", icon="icon")


class BookmarkTypeConnection(graphene.relay.Connection):
    class Meta:
        name = 'BookmarkConnection'
        node = BookmarkType
