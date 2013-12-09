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
        e = Empty()

        for case in [5, 'str', ['arr']]:
            with self.assertRaises(Exception):
                e.validate(case)

    def test_empty(self):
        e = Empty()

        self.assertTrue(e.validate({}))

    def test_non_required(self):
        nri = NonRequiredInt()

        empty = {}
        with_valid_field = {'x': 5}
        with_invalid_field = {'x': 'str'}

        self.assertTrue(nri.validate(empty))
        self.assertTrue(nri.validate(with_valid_field))

        with self.assertRaises(DictValidationException):
            nri.validate(with_invalid_field)

    def test_required(self):
        ri = RequiredInt()

        empty = {}
        with_valid_field = {'x': 5}
        with_invalid_field = {'x': 'str'}

        self.assertTrue(ri.validate(with_valid_field))

        with self.assertRaises(DictValidationException):
            ri.validate(empty)

        with self.assertRaises(DictValidationException):
            ri.validate(with_invalid_field)

    def test_types(self):
        t = TypesDict()

        valid = {'int_field': 5, 'str_field': 'str', 'dict_field': {}, 'list_field': []}

        self.assertTrue(t.validate(valid))

    def test_array_field(self):
        a = ArrayDict()

        valid1 = {'x': [1, 2, 3]}
        valid2 = {'x': []}
        invalid1 = {}
        invalid2 = {'x': 5}
        invalid3 = {'x': {'str': 5}}

        for v in valid1, valid2:
            self.assertTrue(a.validate(v))
        for i in invalid1, invalid2, invalid3:
            with self.assertRaises(DictValidationException):
                a.validate(i)

    def test_sub_dict(self):
        d = DictDict()

        v_types = {'int_field': 5, 'str_field': 'str', 'dict_field': {}, 'list_field': []}
        inv_types = {}

        v_dd = {'x': v_types}
        inv_dd = {'x': inv_types}

        self.assertTrue(d.validate(v_dd))
        with self.assertRaises(DictValidationException):
            d.validate(inv_dd)

    def test_safe_validate(self):
        d = RequiredInt()

        self.assertTrue(d.validate({'x': 5}))

        invalid = {'y': 5}

        # make sure that in the unsafe case, this throws
        # an exception
        with self.assertRaises(DictValidationException):
            d.validate(invalid)

        # when called using safe validation, there
        # should be no exception and just return false
        self.assertFalse(d.validate(invalid, safe=True))


if __name__ == '__main__':
    unittest.main()