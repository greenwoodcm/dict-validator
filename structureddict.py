from meta import StructuredDictMeta


class StructuredDictionary(object):
    __metaclass__ = StructuredDictMeta

    def validate(self, dictionary):
        if not isinstance(dictionary, dict):
            return False

        for fname in self._fields:
            field = self._fields[fname]

            exists = fname in dictionary
            is_valid = exists and self._fields[fname].validate(dictionary[fname])

            # for a field to be valid, there are two possibilities
            #   the field is required and that field exists and validates
            #   the field is not required and that field does not exist or validates
            field_is_valid = (exists and is_valid) if field.required else ((not exists) or is_valid)

            if not field_is_valid:
                return False

        return True