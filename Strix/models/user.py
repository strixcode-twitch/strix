from datetime import datetime
from typing import Dict

from neomodel import UniqueIdProperty, StructuredNode, StringProperty, DateTimeProperty, IntegerProperty, \
    RelationshipTo, Relationship

from Strix.models.bookmark import Bookmark


class User(StructuredNode):
    uid = UniqueIdProperty()
    first_name = StringProperty()
    last_name = StringProperty()
    email = StringProperty()
    password = StringProperty()

    signup_date = DateTimeProperty(default=lambda: datetime.now())

    # Security
    login_ip = StringProperty()
    last_login = DateTimeProperty()
    failed_logins = IntegerProperty(default=0)

    bookmarks = Relationship(Bookmark, 'SAVED')

    def get_gql_node(self) -> Dict:
        return {"first_name": self.first_name, "last_name": self.last_name, "email": self.email, "id": self.uid}
