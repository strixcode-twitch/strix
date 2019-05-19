from neomodel import StructuredNode, UniqueIdProperty, StringProperty, RelationshipFrom, One, RelationshipTo, \
    Relationship


class Folder(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty()

    parent = RelationshipFrom('Folder', 'HAS_FOLDER', cardinality=One)
    children = RelationshipTo('Folder', 'HAS_FOLDER')

    bookmarks = Relationship('Bookmark', 'STORED_IN')

    user = RelationshipFrom('User', 'ROOT_FOLDER')