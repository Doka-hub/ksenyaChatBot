from peewee_async import Manager
from peewee_async.databases import PostgresqlDatabase, MySQLDatabase

from main.loader import settings

database_map = {
    'postgresql': PostgresqlDatabase,
    'mysql': MySQLDatabase,
}

database = database_map[settings.DB_ENGINE](
    database=settings.DB_NAME,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
)
objects = Manager(database)


__all__ = [
    'database',
    'objects',
]
