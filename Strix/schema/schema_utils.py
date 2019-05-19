from typing import Dict


def get_pageinfo_arguments(gql_args: Dict):
    if gql_args.get('first', False) and not gql_args.get('after', False):
        raise Exception('Bad paging')
    if gql_args.get('last', False) and not gql_args.get('before', False):
        raise Exception('Bad paging')
    if gql_args.get('first', False) and (gql_args.get('last', False) or gql_args.get('before', False)):
        raise Exception('Bad paging')
    if gql_args.get('last', False) and ( gql_args.get('first', False) or gql_args.get('after', False)):
        raise Exception('Bad paging')
    
    if gql_args.get('first', False):
        return ((gql_args.get('first'), gql_args.get('after')), (),)