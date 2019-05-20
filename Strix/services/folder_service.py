from neomodel import db

from Strix.models.folder import Folder
from Strix.services.user_service import get_current_user


def folder_get_root(user_id: str) -> Folder:
    user = get_current_user(user_id)
    return user.folders.all()[0]


def create_sub_folder(user_id: str, parent_id: str, name: str) -> Folder:
    user = get_current_user(user_id)
    if user is None:
        # TODO raise better exception
        raise Exception(f'No user with this id {user_id} found.')

    parent: Folder = Folder.nodes.get_or_none(uid=parent_id)
    if parent is None:
        # TODO raise better exception
        raise Exception(f'Folder with id {parent_id} does not exist.')

    if not is_folder_connected_to_user(user.uid, parent.uid):
        # TODO raise better exception
        raise Exception(f'Folder with id {parent_id} does not exist.')

    entity = Folder(name=name).save()
    parent.children.connect(entity)

    return entity


def get_folder(user_id: str, folder_id: str) -> Folder:
    user = get_current_user(user_id)

    if folder_id is None:
        return user.folders.all()[0]

    folder = Folder.nodes.get_or_none(uid=folder_id)
    if folder is None:
        # TODO better exception
        raise Exception("Folder not found")

    if not is_folder_connected_to_user(user.uid, folder.uid):
        # TODO better exception
        raise Exception("Folder not found")

    return folder


def is_folder_connected_to_user(user_id: str, folder_id: str):
    results, _ = db.cypher_query(
        f'match (u:User {{uid: "{user_id}"}})-[:ROOT_FOLDER]->(:Folder)-[:HAS_FOLDER*1..]->(f:Folder {{uid: "{folder_id}"}}) return u,f', )

    return len(results) != 0