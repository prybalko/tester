""" Data storage models """

import datetime
import os

from peewee import AutoField, DateTimeField, TextField, Model, IntegerField

from tester import DB


class Test(Model):
    """ The main model for storing tests metadata. """
    id = AutoField()
    pid = IntegerField(default=os.getpid)
    environment = TextField(default='local')
    test = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    started_at = DateTimeField(null=True)
    finished_at = DateTimeField(null=True)
    status = TextField(default='pending', index=True)
    logs = TextField(null=True)

    class Meta:
        database = DB
