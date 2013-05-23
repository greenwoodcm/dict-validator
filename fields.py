

class Field(object):

    def __init__(self, ftype, required=True):
        self.ftype = ftype
        self.required = required

    def validate(self, value):
        return isinstance(value, self.ftype)


class ArrayField(Field):

    """
    ftype will be another Field definition that we use
    to validate each element in the array
    """

    def validate(self, value):
        if not isinstance(value, list):
            return False

        for val in value:
            elem_is_valid = self.ftype.validate(val)
            if not elem_is_valid:
                return False
        return True


class StructuredDictField(Field):

    """
    ftype will be itself a StructuredDictionary type
    """

    def validate(self, value):
        if not isinstance(value, dict):
            return False

        sd = self.ftype()
        return sd.validate(value)