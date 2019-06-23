"""
tester: advanced unit and functional testing with Python.
"""
import os

from peewee import SqliteDatabase

module_path = os.path.dirname(os.path.realpath(__file__))

DB = SqliteDatabase(f'{module_path}/tester.db')
