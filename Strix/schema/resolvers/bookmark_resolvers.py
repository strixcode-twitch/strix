from typing import List

import graphene

from Strix.models.bookmark import Bookmark
from Strix.schema.input_types.bookmark_input_type import BookmarkInputType
from Strix.schema.types.bookmark_type import BookmarkType
from Strix.services.bookmark_service import bookmark_create_or_add_relation
from Strix.services.user_service import get_current_user


def resolve_bookmarks(self, info, **args) -> List[BookmarkType]:
    user = get_current_user(args.get('user_id'))
    if user.bookmarks is None:
        return []

    bookmarks: List[Bookmark] = user.bookmarks
    return [BookmarkType(**x.get_gql_node()) for x in bookmarks]


class CreateBookmark(graphene.Mutation):
    class Arguments:
        bookmark = BookmarkInputType(required=True)
        tags = graphene.List(graphene.String)
        folder_id = graphene.ID(description="Id of the folder you want to place this bookmark in, defaults to root folder.")

    Output = BookmarkType

    def mutate(self, info, bookmark: BookmarkInputType, **args):
        user = get_current_user(args.get('user_id'))
        entity: Bookmark = bookmark_create_or_add_relation(
            user,
            {"url": bookmark.url},
            args.get('tags', []),
            args.get('folder_id', None)
        )

        return BookmarkType(**entity.get_gql_node())
