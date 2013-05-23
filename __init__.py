from meta import StructuredDictMeta
from fields import *


class StructuredDictionary(object):
    __metaclass__ = StructuredDictMeta

    def validate(self, dictionary):
        print str(self._fields)

        for fname in self._fields:
            field = self._fields[fname]

            # if its required, it must be there and the type must be valid
            if field.required:
                is_valid = self._fields[fname].validate(dictionary[fname])
                if not is_valid:
                    return False

            # otherwise it must either not exist OR the type must be valid
            else:
                exists = fname in self._dict
                is_valid = not exists or self._fields[fname].validate(dictionary[fname])
                if not is_valid:
                    return False

        return True


class Friend(StructuredDictionary):
    _id = Field(int)
    name = Field(str)


class Person(StructuredDictionary):
    y = 5
    f = Field(int)
    g = ArrayField(Field(str), required=True)
    h = StructuredDictField(Friend)

p = Person()
d = {'f': 5, 'g': [''], 'h': {'_id': 123, 'name': 'Chris'}}

print str(p.validate(d))