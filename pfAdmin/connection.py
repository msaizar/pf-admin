import MySQLdb
from pfAdmin.utils import Config


class AbstractDB:
    """docstring for AbstractDB"""

    class __impl():

        def __init__(self):
            Co = Config()
            if Co.is_parsed() == False:
                Co.parse_config()
            self.config = Co.get_config()
            self.db = MySQLdb.connect(
                user=self.config['username'],
                passwd=self.config['password'],
                host=self.config['hostname'],
                db=self.config['database'],
                unix_socket=self.config['socket'])

        def commit(self):
            return self.db.commit()

        def info(self):
            return self.db.info()

        def rollback(self):
            return self.db.rollback()

        def cursor(self):
            c = self.db.cursor()
            return c

    __instance = None

    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if AbstractDB.__instance is None:
            # Create and remember instance
            AbstractDB.__instance = AbstractDB.__impl()

        # Store instance reference as the only member in the handle
        self.__dict__['_AbstractDB__instance'] = AbstractDB.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)
