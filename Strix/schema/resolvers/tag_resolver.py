import graphene
from graphql import ResolveInfo

from Strix.schema.input_types.tag_input_type import TagInputType
from Strix.schema.types.bookmark_type import BookmarkType
from Strix.schema.types.tag_type import TagType
from Strix.services.tag_service import tag_create_or_add_relation
from Strix.services.user_service import get_current_user


class CreateTag(graphene.Mutation):
    class Arguments:
        tag = TagInputType(required=True)

    Output = TagType

    def mutate(self, info, tag: TagInputType, **args):
        user = get_current_user(args.get('user_id'))

        entity = tag_create_or_add_relation(user, {"name": tag.name, 'bookmark_id': tag.bookmark_id})

        return TagType(**entity.get_gql_node())
