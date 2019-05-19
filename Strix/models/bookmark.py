from typing import Dict

from neomodel import UniqueIdProperty, StructuredNode, StringProperty, RelationshipFrom


class Bookmark(StructuredNode):
    uid = UniqueIdProperty()
    url = StringProperty()
    title = StringProperty()

    def get_gql_node(self) -> Dict:
        return {"id": self.uid, "url": self.url, "title": self.title}