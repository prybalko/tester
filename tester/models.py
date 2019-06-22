import datetime

from peewee import *

db = SqliteDatabase('my_database.db')


class Test(Model):
    id = AutoField()
    environment = TextField(default='local')
    test = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    started_at = DateTimeField(null=True)
    finished_at = DateTimeField(null=True)
    status = TextField(default='pending')
    logs = TextField(null=True)

    class Meta:
        database = db
