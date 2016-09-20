"""
A wrapper around python-arango's database class adding some SQLAlchemy like ORM methods to it.
"""
from inspect import isclass

from arango.database import Database as ArangoDatabase
from .collections import CollectionBase


class Query(object):
    """
    Class used for querying records from an arangodb collection using a database connection
    """

    def __init__(self, CollectionClass, db=None):

        self._db = db
        self._CollectionClass = CollectionClass
        self._bind_vars = {'@collection': self._CollectionClass.__collection__}

    def count(self):
        "Return collection count"

        return self._db.collection(self._CollectionClass.__collection__).count()

    def all(self):
        "Return all records considering current filter conditions (if any)"

        aql = 'FOR rec IN @@collection RETURN rec'

        results = self._db.aql.execute(aql, bind_vars=self._bind_vars)
        ret = []

        for rec in results:
            ret.append(self._CollectionClass._load(rec))

        #print([student['name'] for student in result])
        return ret