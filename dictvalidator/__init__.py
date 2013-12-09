__import__('pkg_resources').declare_namespace(__name__)

from meta import DictValidatorMeta
from exceptions import *


class DictValidator(object):
    __metaclass__ = DictValidatorMeta

    def __init__(self, dictionary):
        self.dictionary = dictionary

    def validate(self, safe=False):
        validation_errors = []

        if not isinstance(self.dictionary, dict):
            validation_errors.append(
                Exception('DictValidator attempted to validate non-dict type'))
        else:
            for fname in self._fields:
                field = self._fields[fname]

                # first check if it exists and add an error if it is absent
                exists = fname in self.dictionary
                if not exists:
                    if field.required:
                        validation_errors.append(FieldAbsentException(fname))
                    continue

                # now that we know its there, validate it
                try:
                    self._fields[fname].validate(self.dictionary[fname])
                except DictValidationException as e:
                    validation_errors.append(e)

        # return the result
        is_valid = len(validation_errors) == 0
        if is_valid:
            return True

        if safe:
            return False

        raise DictValidationException(validation_errors)