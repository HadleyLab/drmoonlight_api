from django.db.backends.postgresql_psycopg2 import base


class DatabaseWrapper(base.DatabaseWrapper):
    def on_commit(self, callback):
        callback()
