from typing import Dict

from Strix.models.folder import Folder
from Strix.models.user import User
from Strix.models.user import Bookmark
from Strix.services.folder_service import is_folder_connected_to_user
from Strix.services.tag_service import tag_create_or_add_relation


def bookmark_create_or_add_relation(user: User, bookmark: Dict, tags=[], folder_id=None) -> Bookmark:
    existing = Bookmark.nodes.get_or_none(url=bookmark.get('url'))
    if existing and user.bookmarks.is_connected(existing):
        raise Exception('You have already bookmarked this page.')

    new_bookmark = existing if existing is not None else Bookmark(url=bookmark.get('url'))
    new_bookmark.save()

    user.bookmarks.connect(new_bookmark)

    for tag in tags:
        tag_create_or_add_relation(user, {'bookmark_id': new_bookmark.uid, 'name': tag})

    if folder_id is not None:
        if not is_folder_connected_to_user(user.uid, folder_id):
            # TODO better exception
            raise Exception('Folder does not exist.')

        folder = Folder.nodes.get_or_none(uid=folder_id)
        if folder is None:
            # TODO better exception
            raise Exception('Folder does not exist.')

        folder.bookmarks.connect(new_bookmark)
    else:
        root_folder: Folder = user.folders.all()[0]
        root_folder.bookmarks.connect(new_bookmark)

    return new_bookmark


def get_bookmark(bookmark_id: str) -> Bookmark:
    return Bookmark.nodes.get_or_none(uid=bookmark_id)
