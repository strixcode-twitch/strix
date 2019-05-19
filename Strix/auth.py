from datetime import datetime

import jwt
from graphql import ResolveInfo, GraphQLError
from sanic.request import Request
from sanic_jwt import Configuration

# TODO Place somewhere else.
from sanic_jwt.exceptions import AuthenticationFailed

from Strix.models.user import User
from Strix.dtos.login_request import LoginRequest
from Strix.services.user_service import verify_password

SECRET = 'secret'


async def authenticate(request: Request):
    login_request = LoginRequest(**request.json)

    user = User.nodes.get_or_none(email=login_request.email)
    if user is None:
        raise AuthenticationFailed('Wrong email and or password.')

    correct_password = verify_password(login_request.password, user.password)
    if not correct_password:
        user.failed_logins = user.failed_logins + 1
        user.save()
        raise AuthenticationFailed('Wrong email and or password')

    user.last_login = datetime.now()
    user.login_ip = request.ip # TODO verify that this is the correct remote address.
    user.save()

    return dict(user_id=user.id)


async def retrieve_user(request, payload, *args, **kwargs):
    if payload:
        user_id = payload.get('user_id', None)
        return {'user_id': user_id, 'first_name': 'Sindre'}
    else:
        return None


class SanicConfiguration(Configuration):
    algorithm = 'HS256'
    secret = SECRET
    expiration_delta = 60 * 10000000 # TODO fix expiration


class AuthorizationMiddleware(object):
    def resolve(next, root, info: ResolveInfo, **args):
        request: Request = info.context.get('request', None)
        if request is None:
            raise GraphQLError("Bad request")

        # Cannot include user_id if it is a introspection query
        if '__schema' in info.path:
            return next(root, info, **args)

        token: str = request.headers.get('authorization').split('Bearer ')[1]
        message_received = jwt.decode(token, SECRET)
        user_id = message_received.get('user_id', None)
        if user_id is None:
            raise GraphQLError('Bad request')
        return next(root, info, **{'user_id': user_id, **args})
