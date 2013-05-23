from fields import *


class StructuredDictMeta(type):

    def __init__(cls, name, bases, namespace):
        # the _fields attribute will hold a mapping from
        # field names to their Field instances
        cls._fields = {}

        for (key, value) in namespace.items():
            if isinstance(value, Field):
                cls._fields[key] = value