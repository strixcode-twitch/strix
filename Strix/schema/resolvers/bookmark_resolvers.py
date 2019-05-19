import graphene

from Strix.schema.input_types.bookmark_input_type import BookmarkInputType
from Strix.schema.types.bookmark_type import BookmarkType
from Strix.services.bookmark_service import create_or_add_relation
from Strix.services.user_service import get_current_user


def get_bookmark(id):
    return BookmarkType(uid=id, title="Title", url="url", description="description", icon="icon")


def resolve_bookmarks(self, info, **args):
    return [get_bookmark(str(x)) for x in range(5)]


class CreateBookmark(graphene.Mutation):
    class Arguments:
        bookmark = BookmarkInputType(required=True)

    Output = BookmarkType

    def mutate(self, info, bookmark: BookmarkInputType, **args):
        user = get_current_user(args.get('user_id'))
        entity = create_or_add_relation(user, {"url": bookmark.url})
        return BookmarkType(**entity.get_gql_node())
