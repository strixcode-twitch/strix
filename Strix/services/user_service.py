from Strix.models.user import User
from Strix.dtos.rest_user_input import RestUserInput
from passlib.hash import argon2

def create_user(user: RestUserInput):
    existing = User.nodes.get_or_none(email=user.email)
    if existing is not None:
        raise Exception('Email already in use')

    new_user = User(**user.__dict__)
    new_user.password = hash_password(user.password)
    # TODO hash passsword
    new_user.save()
    return new_user.uid


def hash_password(password: str) -> str:
    return argon2.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return argon2.verify(password, hash)


def get_current_user(user_id: str):
    return User.nodes.get_or_none()