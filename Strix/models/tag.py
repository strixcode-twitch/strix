from datetime import datetime
from typing import Dict

from neomodel import UniqueIdProperty, StructuredNode, StringProperty, StructuredRel, DateTimeProperty


class Tag(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty()

    def get_gql_node(self) -> Dict:
        return {"id": self.uid, "name": self.name}


class TaggedRel(StructuredRel):
    by = StringProperty()
    created_date = DateTimeProperty(default=lambda: datetime.now())
