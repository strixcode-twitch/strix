class StrixStructuredNodeMixin(object):
    def as_dict(self, ignore=[]):
        my_dict = self.__properties__
        if my_dict.get('id'):
            del my_dict['id']

        if my_dict.get('uid'):
            my_dict['id'] = my_dict['uid']
            del my_dict['uid']

        for p in ignore:
            if my_dict.get(p):
                del my_dict[p]

        return my_dict