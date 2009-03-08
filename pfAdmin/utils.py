from string import split
from pfAdmin.error import InvalidUsernameFormatError
from pfAdmin.error import ConfigNotFoundError
import ConfigParser
import MySQLdb
from os.path import lexists
import md5

def encrypt_password(password):

    new_pass = md5.new(password).hexdigest()
    return new_pass
        
def get_config(path):
    
    """Method that returns connection configuration"""
    config = {
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
    if path is not '' and not lexists(path):
        raise ConfigNotFoundError(path)
    configp.read(path)
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
                    config[var_name] = v
                else:
                    config[var_name + '.' + k] = v
            else:
                config[k] = v
    return config

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