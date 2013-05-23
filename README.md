dict-validator
==============

Python module for validating dictionaries against a schema.  I built this module for use in a Flask web service that accepts JSON data and must validate it before proceeding.

Features
---

* express a dictionary schema in a clear, object-oriented manner
* type-check various attributes of the dictionary
* specify whether an attribute should be required or optional
* support for list types
* support for nested schemas

Example
---

```
class InnerDict(DictValidator):
  x = Field(int)                      # x is a required attribute and must be an integer
  y = Field(str, required=False)      # y is an optional attribute, and should be a string if it exists
  z = ArrayField(str)                 # z is a required array of strings
  
class MyDict(DictValidator):
  a = StructuredDictField(InnerDict)  # a is a required dictionary attribute that conforms to the schema above


dict1 = {}
dict2 = {'a': 5}
dict3 = {'a': {}}
dict4 = {'a': {'x': 5, 'y': 'string', 'z': ['a','b','c']}}

validator = MyDict()

valid1 = validator.validate(dict1)    # invalid because the dict does not contain a
valid2 = validator.validate(dict2)    # invalid because a is not a dict
valid3 = validator.validate(dict3)    # invalid because a fails the InnerDict validator
valid4 = validator.validate(dict4)    # valid
```

Improvements
---

* add validators to individual fields (range validation on integers, length validation for strings, etc.)
* add support for attribute names that are reserved keywords in python.  maybe escape with a double underscore.
* clean the code so that you don't have to instantiate an instance of the validator.  Another clean option would be to wrap the dictionary in your validation class and then validate that way

for example:
```
d = MyDict({'a': [1, 2, 3]})
d.validate()
```
