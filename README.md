dict-validator
==============

Python module for validating dictionaries against a schema.  

I built this module for use in a Flask web service that accepts JSON data and must validate 
it before proceeding.  I first considered using [Voluptuous](https://pypi.python.org/pypi/voluptuous/), 
which has a similar end result.  However, I don't really like the method they use of defining the
schema itself as a dictionary.  So I have created an object-oriented method of validating dictionaries,
where you define your schema as a class or set of nested classes that indicate which attributes should
exist in the dictionary.

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


dict1 = MyDict({})
dict2 = MyDict({'a': 5})
dict3 = MyDict({'a': {}})
dict4 = MyDict({'a': {'x': 5, 'y': 'string', 'z': ['a','b','c']}})

valid1 = dict1.validate()    # invalid because the dict does not contain a
valid2 = dict2.validate()    # invalid because a is not a dict
valid3 = dict3.validate()    # invalid because a fails the InnerDict validator
valid4 = dict4.validate()    # valid
```

Improvements
---

* add validators to individual fields (range validation on integers, length validation for strings, etc.)
* add support for attribute names that are reserved keywords in python.  maybe escape with a double underscore.

