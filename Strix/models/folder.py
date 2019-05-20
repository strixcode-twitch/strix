from typing import Dict

from neomodel import StructuredNode, UniqueIdProperty, StringProperty, RelationshipFrom, One, RelationshipTo, \
    Relationship


class Folder(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty()

    parent = RelationshipFrom('Folder', 'HAS_FOLDER', cardinality=One)
    children = RelationshipTo('Folder', 'HAS_FOLDER')

    bookmarks = Relationship('Strix.models.bookmark.Bookmark', 'STORED_IN')

    user = RelationshipFrom('Strix.models.user.User', 'ROOT_FOLDER')

    def get_gql_node(self) -> Dict:
        return {"id": self.uid, "name": self.name}
