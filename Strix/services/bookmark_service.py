from typing import Dict

from Strix.models.user import User
from Strix.models.user import Bookmark


def create_or_add_relation(user: User, bookmark: Dict) -> Bookmark:
    url = bookmark.get('url')

    existing = Bookmark.nodes.get_or_none(url=bookmark.get('url'))
    new_bookmark = existing if existing is not None else Bookmark(url=bookmark.get('url'))
    new_bookmark.save()

    user.bookmarks.connect(new_bookmark)

    return new_bookmark