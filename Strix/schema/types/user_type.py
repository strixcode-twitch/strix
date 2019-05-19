import graphene


class UserType(graphene.ObjectType):
    class Meta:
        name = 'User'

    uid = graphene.NonNull(graphene.ID)
    first_name = graphene.String()
    last_name = graphene.String()
    full_name = graphene.String()
    email = graphene.String()

    def resolve_full_name(root, info):
        return '{} {}'.format(root.first_name, root.last_name)
