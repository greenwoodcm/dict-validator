import unittest
from structureddict import StructuredDictionary
from fields import *

# ----- StructuredDictionary subclasses used for testing ----------------------


class Empty(StructuredDictionary):
    pass


class RequiredInt(StructuredDictionary):
    x = Field(int, required=True)


class NonRequiredInt(StructuredDictionary):
    x = Field(int, required=False)


class TypesDict(StructuredDictionary):
    int_field = Field(int)
    str_field = Field(str)
    dict_field = Field(dict)
    list_field = Field(list)


class ArrayDict(StructuredDictionary):
    x = ArrayField(Field(int))


class DictDict(StructuredDictionary):
    x = StructuredDictField(TypesDict)

# ----- Test cases ------------------------------------------------------------


class TestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_non_dict(self):
        e = Empty()

        self.assertFalse(e.validate(5))
        self.assertFalse(e.validate('str'))
        self.assertFalse(e.validate(['arr']))

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
        self.assertFalse(nri.validate(with_invalid_field))

    def test_required(self):
        ri = RequiredInt()

        empty = {}
        with_valid_field = {'x': 5}
        with_invalid_field = {'x': 'str'}

        self.assertFalse(ri.validate(empty))
        self.assertTrue(ri.validate(with_valid_field))
        self.assertFalse(ri.validate(with_invalid_field))

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
            self.assertFalse(a.validate(i))

    def test_sub_dict(self):
        d = DictDict()

        v_types = {'int_field': 5, 'str_field': 'str', 'dict_field': {}, 'list_field': []}
        inv_types = {}

        v_dd = {'x': v_types}
        inv_dd = {'x': inv_types}

        self.assertTrue(d.validate(v_dd))
        self.assertFalse(d.validate(inv_dd))

if __name__ == '__main__':
    unittest.main()