from exceptions import *

class Field(object):

    def __init__(self, ftype, required=True):
        self.ftype = ftype
        self.required = required

        # this is set in the meta when a Field is found
        # as a member of a dictionary object
        self.field_name = ''

    def validate(self, value):
        if not isinstance(value, self.ftype):
            raise FieldTypeValidationException(
                self.field_name,
                self.ftype,
                type(value))


class ArrayField(Field):

    """
    ftype will be another Field definition that we use
    to validate each element in the array
    """
    def __init__(self, subtype, required=True):
        super(ArrayField, self).__init__(list, required)
        self.subtype = subtype

    def validate(self, value):
        super(ArrayField, self).validate(value)

        for val in value:
            self.subtype.validate(val)


class StructuredDictField(Field):

    """
    ftype will be itself a StructuredDictionary type
    """
    def __init__(self, subtype, required=True):
        super(StructuredDictField, self).__init__(dict, required)
        self.subtype = subtype

    def validate(self, value):
        super(StructuredDictField, self).validate(value)

        sd = self.subtype(value)
        return sd.validate()