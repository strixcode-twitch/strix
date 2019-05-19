import uuid

from Strix.schema.types.user_type import UserType


def resolve_user(self, info, **args):
    return UserType(**{'uid': str(uuid.uuid4()), 'first_name': 'Sindre', 'last_name': 'Smistad', 'email': 'sindre@downgoat.net'})
