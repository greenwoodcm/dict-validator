import unittest
from dictvalidator import DictValidator
from dictvalidator.fields import *

# ----- StructuredDictionary subclasses used for testing ----------------------


class Empty(DictValidator):
    pass


class RequiredInt(DictValidator):
    x = Field(int, required=True)


class NonRequiredInt(DictValidator):
    x = Field(int, required=False)


class TypesDict(DictValidator):
    int_field = Field(int)
    str_field = Field(str)
    dict_field = Field(dict)
    list_field = Field(list)


class ArrayDict(DictValidator):
    x = ArrayField(Field(int))


class DictDict(DictValidator):
    x = StructuredDictField(TypesDict)

# ----- Test cases ------------------------------------------------------------


class TestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_non_dict(self):
        for case in [5, 'str', ['arr']]:
            with self.assertRaises(Exception):
                Empty(case).validate()

    def test_empty(self):
        self.assertTrue(Empty({}).validate())

    def test_non_required(self):
        empty = NonRequiredInt({})
        with_valid_field = NonRequiredInt({'x': 5})
        with_invalid_field = NonRequiredInt({'x': 'str'})

        self.assertTrue(empty.validate())
        self.assertTrue(with_valid_field.validate())

        with self.assertRaises(DictValidationException):
            with_invalid_field.validate()

    def test_required(self):
        empty = RequiredInt({})
        with_valid_field = RequiredInt({'x': 5})
        with_invalid_field = RequiredInt({'x': 'str'})

        self.assertTrue(with_valid_field.validate())

        with self.assertRaises(DictValidationException):
            empty.validate()

        with self.assertRaises(DictValidationException):
            with_invalid_field.validate()

    def test_types(self):

        valid = {'int_field': 5, 'str_field': 'str', 'dict_field': {}, 'list_field': []}
        t = TypesDict(valid)

        self.assertTrue(t.validate())

    def test_array_field(self):
        valid1 = {'x': [1, 2, 3]}
        valid2 = {'x': []}
        invalid1 = {}
        invalid2 = {'x': 5}
        invalid3 = {'x': {'str': 5}}

        for v in valid1, valid2:
            self.assertTrue(ArrayDict(v).validate())
        for i in invalid1, invalid2, invalid3:
            with self.assertRaises(DictValidationException):
                ArrayDict(i).validate()

    def test_sub_dict(self):
        v_types = {'int_field': 5, 'str_field': 'str', 'dict_field': {}, 'list_field': []}
        inv_types = {}

        v_dd = DictDict({'x': v_types})
        inv_dd = DictDict({'x': inv_types})

        self.assertTrue(v_dd.validate())
        with self.assertRaises(DictValidationException):
            inv_dd.validate()

    def test_safe_validate(self):
        valid = RequiredInt({'x': 5})

        self.assertTrue(valid.validate())

        invalid = RequiredInt({'y': 5})

        # make sure that in the unsafe case, this throws
        # an exception
        with self.assertRaises(DictValidationException):
            invalid.validate()

        # when called using safe validation, there
        # should be no exception and just return false
        self.assertFalse(invalid.validate(safe=True))


if __name__ == '__main__':
    unittest.main()