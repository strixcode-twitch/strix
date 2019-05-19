from typing import Dict

from Strix.models.bookmark import Bookmark
from Strix.models.tag import Tag
from Strix.models.user import User
from neomodel import db


def tag_create_or_add_relation(user: User, tag: Dict) -> Tag:
    bookmark = Bookmark.nodes.get_or_none(uid=tag.get('bookmark_id'))
    if bookmark is None:
        # TODO Raise a better exception.
        raise Exception('Cannot add a tag to a non existing bookmark.')

    existing = Tag.nodes.get_or_none(name=tag.get('name'))
    new_tag = existing if existing is not None else Tag(name=tag.get('name')).save()

    has_relation = user.tags.is_connected(new_tag)
    if not has_relation:
        user.tags.connect(new_tag)

    results, _ = db.cypher_query(f'match (:User {{uid: "{user.uid}"}})-[:SAVED]-(b:Bookmark {{uid:"{bookmark.uid}"}})-[:TAGGED]-(t:Tag {{uid: "{new_tag.uid}"}}) return b,t',)
    if len(results) == 0:
        bookmark.tags.connect(new_tag, {'by': user.uid})
    else:
        # TODO better exception
        # TODO Maybe this shouldnt raise a exception, maybe just return.
        raise Exception('Duplicate tag')

    return new_tag


def get_bookmark_tags(bookmark: Bookmark, user: User):
    return bookmark.tags.match(by=user.uid).all()

