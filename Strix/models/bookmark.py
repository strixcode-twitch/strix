from typing import Dict

from neomodel import UniqueIdProperty, StructuredNode, StringProperty, Relationship, RelationshipTo

from Strix.models.folder import Folder
from Strix.models.tag import Tag, TaggedRel


class Bookmark(StructuredNode):
    uid = UniqueIdProperty()
    url = StringProperty()
    title = StringProperty()

    tags = RelationshipTo(Tag, 'TAGGED', model=TaggedRel)
    folder = Relationship(Folder, 'STORED_IN')

    def get_gql_node(self) -> Dict:
        return {"id": self.uid, "url": self.url, "title": self.title}