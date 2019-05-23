from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS
from sanic_graphql import GraphQLView
from sanic_jwt import Initialize, protected, inject_user

from Strix.auth import SanicConfiguration, retrieve_user, authenticate, SECRET, AuthorizationMiddleware
from Strix.dtos.rest_user_input import RestUserInput
from Strix.models.user import User
from Strix.schema.schema import schema
from Strix.services.user_service import create_user

app = Sanic()
Initialize(app, authenticate=authenticate, retrieve_user=retrieve_user, configuration_class=SanicConfiguration)
CORS(app)

from neomodel import config
config.DATABASE_URL = 'bolt://neo4j:123qwe@localhost:7687' # TODO move to setting file.


class SanixGraphql(GraphQLView):
    schema = schema
    graphiql = True
    decorators = [protected(), inject_user()]
    middleware = [AuthorizationMiddleware]


@app.route("/")
async def test(request):
    return json({"hello": "world"})

@app.route("/create_user", methods=['POST'])
async def post_create_user(request):
    user: RestUserInput = RestUserInput(**request.json)

    user_id = create_user(user)

    return json({"hello": "world"})


@app.route("/protected")
@inject_user()
@protected()
async def protected(request, user):
    return json({"hello": "world", 'protected': True, 'user': user})


app.add_route(SanixGraphql.as_view(), '/graphql')
