from typing import Dict

from Strix.models.user import User
from Strix.models.user import Bookmark


def bookmark_create_or_add_relation(user: User, bookmark: Dict) -> Bookmark:
    existing = Bookmark.nodes.get_or_none(url=bookmark.get('url'))
    new_bookmark = existing if existing is not None else Bookmark(url=bookmark.get('url'))
    new_bookmark.save()

    user.bookmarks.connect(new_bookmark)

    return new_bookmark


def get_bookmark(bookmark_id: str) -> Bookmark:
    return Bookmark.nodes.get_or_none(uid = bookmark_id)