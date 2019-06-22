from setuptools import setup

setup(
   name='tester',
   version='0.1.0',
   packages=['tester'],
   install_requires=['pytest',
                     'peewee'],
   entry_points={
      'console_scripts': [
         'tester = tester.__main__:main'
      ]
   },
)
