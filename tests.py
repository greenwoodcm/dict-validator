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
        Empty({})

    def test_non_required(self):
        NonRequiredInt({})

        x = NonRequiredInt({'x': 5})
        self.assertEqual(5, x.x)

        with self.assertRaises(DictValidationException):
            NonRequiredInt({'x': 'str'})

    def test_required(self):
        x = RequiredInt({'x': 5})
        self.assertEqual(5, x.x)

        with self.assertRaises(DictValidationException):
            RequiredInt({})

        with self.assertRaises(DictValidationException):
            RequiredInt({'x': 'str'})

    def test_types(self):

        valid = {'int_field': 5, 'str_field': 'str', 'dict_field': {}, 'list_field': []}
        x = TypesDict(valid)

        self.assertEqual(5, x.int_field)
        self.assertEqual('str', x.str_field)
        self.assertEqual({}, x.dict_field)
        self.assertEqual([], x.list_field)

    def test_array_field(self):
        valid1 = ArrayDict({'x': [1, 2, 3]})
        self.assertEqual([1, 2, 3], valid1.x)

        valid2 = ArrayDict({'x': []})
        self.assertEqual([], valid2.x)

        invalid1 = {}
        invalid2 = {'x': 5}
        invalid3 = {'x': {'str': 5}}

        for i in invalid1, invalid2, invalid3:
            with self.assertRaises(DictValidationException):
                ArrayDict(i)

    def test_sub_dict(self):
        v_types = {
            'int_field': 5,
            'str_field': 'str',
            'dict_field': {},
            'list_field': []
        }
        obj = DictDict({'x': v_types})

        self.assertEqual(5, obj.x.int_field)
        self.assertEqual('str', obj.x.str_field)
        self.assertEqual({}, obj.x.dict_field)
        self.assertEqual([], obj.x.list_field)

        inv_types = {}
        with self.assertRaises(DictValidationException):
            DictDict({'x': inv_types})


if __name__ == '__main__':
    unittest.main()