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
    x = ArrayField(int)


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

if __name__ == '__main__':
    unittest.main()