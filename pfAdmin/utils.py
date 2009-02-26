from string import split
from pfAdmin.error import InvalidUsernameFormatError
from pfAdmin.error import ConfigNotFoundError
import ConfigParser
import MySQLdb
from os.path import lexists

class Config:
    """ A python singleton """

    class __impl():
        """ Implementation of the singleton interface """


        def set_path(self, path):
            """ Test method, return singleton id """
            self.path = path
            
        def get_path(self):
            return self.path
        
        def is_parsed(self):
            return self.parsed
        
        def parse_config(self):
            """Method that returns connection configuration"""
            self.config = {
                'hostname': 'localhost',
                'database': 'mailserver',
                'username': 'root',
                'password': 'mypass123',
                'port': '3306',
                'socket': '/var/run/mysqld/mysqld.sock',
                'aliases': 'virtual_aliases',
                'aliases.id': 'id',
                'aliases.source': 'source',
                'aliases.destination': 'destination',
                'aliases.domain_id': 'domain_id',
                'users': 'virtual_users',
                'users.id': 'id',
                'users.domain_id': 'domain_id',
                'users.user': 'user',
                'users.password': 'password',
                'domains': 'virtual_domains',
                'domains.id': 'id',
                'domains.name': 'name',
            }
            result = []
            configp = ConfigParser.SafeConfigParser()
            if self.path is not '' and not lexists(self.path):
                raise ConfigNotFoundError(self.path)
            configp.read(self.path)
            for sec in configp.sections():
                if sec == 'Users Table':
                    var_name = 'users'
                elif sec == 'Domains Table':
                    var_name = 'domains'
                elif sec == 'Aliases Table':
                    var_name = 'aliases'
                else:
                    var_name = None
                for k, v in configp.items(sec):
                    if var_name:
                        if k == 'tname':
                            self.config[var_name] = v
                        else:
                            self.config[var_name + '.' + k] = v
                    else:
                        self.config[k] = v
            self.parsed = True
        
        def get_config(self):
            return self.config

    # storage for the instance reference
    __instance = None


    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if Config.__instance is None:
            # Create and remember instance
            Config.__instance = Config.__impl()
            self.path = ''
            self.config = {}
            self.parsed = False
        # Store instance reference as the only member in the handle
        self.__dict__['_Config__instance'] = Config.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)

def connect_db(config):
    db = MySQLdb.connect(user=config['username'],
    passwd=config['password'],
    host=config['hostname'],
    db=config['database'],
    unix_socket=config['socket'])
    return db

def parse_email(email):
    temp = split(email,'@')
    if len(temp) != 2 or temp[0] == '' or temp[1] == '':
        raise InvalidUsernameFormatError
    else:
        return temp[0], temp[1]