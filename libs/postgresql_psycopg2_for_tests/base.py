from django.db.backends.postgresql_psycopg2 import base

from django.conf import settings


class DatabaseWrapper(base.DatabaseWrapper):
    def on_commit(self, callback):
        if getattr(settings, 'SYNC_ON_COMMIT', True):
            callback()
        else:
            super(DatabaseWrapper, self).on_commit(callback)
