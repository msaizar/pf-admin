#!/usr/bin/env python
import sys
from pfAdmin.mail import Mail
from optparse import OptionParser
from pfAdmin.utils import parse_email, get_config
from pfAdmin.error import UserFoundError, UserNotFoundError
from pfAdmin.error import DomainFoundError, DomainNotFoundError
from pfAdmin.error import InvalidUsernameFormatError
from pfAdmin.error import AliasFoundError, AliasNotFoundError
from pfAdmin.error import ConfigNotFoundError


def __get_option(text):
    option = raw_input('%s [Y/n]' % text)
    if option in ['', 'Y', 'y']:
        return True
    else:
        return False

def __get_alias():
    alias = raw_input('Please input a destination for this source: ')
    return alias

def __get_pass():
    password = raw_input('Please enter the password: ')
    return password
        
def password(username):
    password = __get_pass()
    try: 
        c.update_password(username, password)
        print >> sys.stdout, 'Password updated.'
        raise SystemExit
    except UserNotFoundError:
        print >> sys.stderr, '%s: User does not exist.' % username
        raise SystemExit, 1
    except InvalidUsernameFormatError:
        print >> sys.stderr, '%s: Username format is not valid.' % username
        raise SystemExit, 2
        
def add_user(username):
    password = __get_pass()
    try:
        c.add_user(username,password)
        print >> sys.stdout, 'User added.'
        raise SystemExit
    except DomainNotFoundError:
        print >> sys.stderr, '%s: Domain does not exist.' % username
        flag_opt = __get_option('Create domain and add user?')
        if flag_opt:
            user, domain = parse_email(username)
            c.add_domain(domain)
            c.add_user(username,password)
            print >> sys.stdout, 'User and domain added.'
            raise SystemExit
        else:
            print >> sys.stdout, 'Aborted.'
            raise SystemExit
    except InvalidUsernameFormatError:
        print >> sys.stderr, '%s: Username format is not valid.' % username
        raise SystemExit, 2   
    except UserFoundError:
        print >> sys.stderr, '%s: Username already exists.' % username
        raise SystemExit, 1
        
                 
        
def delete_user(username):
    try:
        c.delete_user(username)
        print >> sys.stdout, 'User deleted.'
        raise SystemExit
    except UserNotFoundError:
        print >> sys.stderr, '%s: User does not exist.' % username
        raise SystemExit, 1
    except InvalidUsernameFormatError:
        print >> sys.stderr, '%s: Username format is not valid.' % username
        raise SystemExit, 2        
        
def list_domains():
    domains = c.list_domains()
    print >> sys.stdout, 'Domains in server:'
    for d in domains:
        print >> sys.stdout, '\t %s' % d
    raise SystemExit

def add_alias(source, destination=None):
    if not destination:
        destination = __get_alias()
    try:
        c.add_alias(source, destination)
        print >> sys.stdout, 'Alias added.'
        raise SystemExit
    except AliasFoundError:
        print >> sys.stderr, '%s -> %s: Alias already exists.' % \
        (source, destination)
        raise SystemExit, 1

def del_alias(source, destination=None):
    if not destination:
        destination = __get_alias()
    try:
        c.delete_alias(source, destination)
        print >> sys.stdout, 'Alias deleted.'
        raise SystemExit
    except AliasNotFoundError:
        print >> sys.stderr, '%s -> %s: Alias does not exist.' % \
        (source, destination)
        raise SystemExit, 1
    
def list_aliases(source):
    try:
        aliases = c.list_aliases(source)
        print >> sys.stdout, 'Aliases for source %s: ' % source
        for a in aliases:
            print >> sys.stdout, '\t %s' % a
        raise SystemExit
    except AliasNotFoundError:
        print >> sys.stderr, '%s: Alias does not exist.' % source
        raise SystemExit, 1
                
def add_domain(server):
    try: 
        c.add_domain(server)
        print >> sys.stdout, 'Domain added.'
        raise SystemExit
    except DomainFoundError:
        print >> sys.stderr, '%s: Domain already exists.' % server
        raise SystemExit, 1

def list_users(domain):
    try:
        users = c.list_users(domain)
        print >> sys.stdout, 'Users in %s: ' % domain
        for u in users:
            print >> sys.stdout, '\t %s' % u
        raise SystemExit
    except DomainNotFoundError:
        print >> sys.stderr, '%s: Domain does not exist.' % domain
        raise SystemExit, 1        

def delete_domain(server):
    try:
        c.delete_domain(server)
        print >> sys.stdout, 'Domain deleted.'
        raise SystemExit
    except DomainNotFoundError:
        print >> sys.stderr, '%s: Domain does not exist.' % server
        raise SystemExit, 1
            
        
def main():
    usage = "usage: %prog option [-c file]"
    parser = OptionParser(usage)
    parser.add_option("--add-user", dest="add_user",
                        help="add USER@DOMAIN", metavar="USER@DOMAIN")
    parser.add_option("--del-user", dest="del_user",
                        help="delete USER@DOMAIN", metavar="USER@DOMAIN")
    parser.add_option("--password", dest="password",
                        help="update password of USER@DOMAIN", 
                        metavar="USER@DOMAIN")
    parser.add_option("--list-users", dest="list_user",
                        help="list users from DOMAIN", metavar="DOMAIN")
    parser.add_option("--add-domain", dest="add_domain",
                        help="add DOMAIN", metavar="DOMAIN")
    parser.add_option("--del-domain", dest="del_domain",
                        help="delete DOMAIN", metavar="USER@DOMAIN")
    parser.add_option("--list-domains", dest="list_domain", 
                        action="store_true", default=False, 
                        help="list domains")
    parser.add_option("--add-alias", dest="add_alias",
                        help="create alias for source USER@DOMAIN " + 
                        "(optionally with -d)", 
                        metavar="USER@DOMAIN")
    parser.add_option("--del-alias", dest="del_alias",
                        help="delete alias for source USER@DOMAIN " + 
                        "(optionally with -d)", 
                        metavar="USER@DOMAIN")
    parser.add_option("--list-aliases", dest="list_alias",
                        help="list aliases for source USER@DOMAIN", 
                        metavar="USER@DOMAIN")
    parser.add_option("-d", dest="dest_alias",
                        help="destination for alias",
                        metavar="DESTINATION")
    parser.add_option("-c", dest="filepath",
                        help="use FILEPATH as configuration file")
                        
    (options, args) = parser.parse_args()
    filepath = ''
    global c
    if hasattr(options,'filepath') and options.filepath != None:
        filepath = options.filepath
    try:
        config = get_config(filepath) 
        c = Mail(config)
    except ConfigNotFoundError:
        print >> sys.stderr, '%s: Configuration file not found.' % filepath
        raise SystemExit, 1
    if hasattr(options,'add_domain') and options.add_domain != None:
        add_domain(options.add_domain)
    elif hasattr(options,'del_domain') and options.del_domain != None:
        delete_domain(options.del_domain)
    elif hasattr(options,'add_user') and options.add_user != None:
        add_user(options.add_user)
    elif hasattr(options,'del_user') and options.del_user != None:
        delete_user(options.del_user)
    elif hasattr(options,'password') and options.password != None:
        password(options.password)
    elif hasattr(options,'list_user') and options.list_user != None:
        list_users(options.list_user)
    elif hasattr(options,'list_domain') and options.list_domain != False:
        list_domains()
    elif hasattr(options,'list_alias') and options.list_alias != None:
        list_aliases(options.list_alias)
    elif hasattr(options, 'add_alias') and options.add_alias != None:
        add_alias(options.add_alias, options.dest_alias)
    elif hasattr(options, 'del_alias') and options.del_alias != None:
        del_alias(options.del_alias, options.dest_alias)
    else:
        parser.print_help()
        raise SystemExit, 2
                        
    

if __name__ == '__main__':
    main()
