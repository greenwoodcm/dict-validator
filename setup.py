"""
dict-validator
-------------

Description goes here...

Links
`````

"""
from setuptools import setup


setup(
    name='dict-validator',
    version='0.1',
    url='https://github.com/greenwoodcm/dict-validator',
    license='BSD',
    author='Chris Greenwood',
    author_email='greenwoodcm@gmail.com',
    description='Python module for validating dictionaries against a schema',
    long_description=__doc__,
    packages=['flaskext'],
    namespace_packages=['flaskext'],
    zip_safe=False,
    platforms='any',
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)