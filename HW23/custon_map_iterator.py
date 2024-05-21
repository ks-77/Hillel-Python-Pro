class CustomMapIterator:
    def __init__(self, data: dict, key_func, value_func):
        self.data = iter(data.items())
        self.key_func = key_func
        self.value_func = value_func

    def __iter__(self):
        return self

    def __next__(self):
        try:
            key, value = next(self.data)
            new_key, new_value = self.key_func(key), self.value_func(value)
            return new_key, new_value
        except StopIteration:
            raise StopIteration
