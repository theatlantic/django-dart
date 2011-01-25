import os
from setuptools import setup, find_packages

from dart import VERSION


f = open(os.path.join(os.path.dirname(__file__), 'README.txt'))
readme = f.read()
f.close()

setup(
    name='django-dart',
    version=".".join(map(str, VERSION)),
    description='django-dart is a reusable Django application for DoubleClick ad tags',
    long_description=readme,
    author='Josh West',
    author_email='',
    url='https://github.com/theatlantic/django-dart',
    packages=find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)

