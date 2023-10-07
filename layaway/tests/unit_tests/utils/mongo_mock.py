class MongoMock(dict):
    """
    Class created to support the generation of Mongo connection Mocks.
    """
    def __init__(self, dict_data):
        self.update(dict_data)

    def __getattr__(self, key):
        if key not in self:
            cls_name = self.__class__.__name__
            msg = f"'{cls_name}' object has no attribute '{key}'"
            raise AttributeError(msg)
        return self.get(key)

    def __setattr__(self, key, value):
        self.update({key: value})

    def find_one(self, *_args):
        return self

    def update_one(self, *_args, **_kwargs):
        return self
