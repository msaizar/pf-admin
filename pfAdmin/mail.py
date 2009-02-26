from pfAdmin.error import DomainFoundError, DomainNotFoundError
from pfAdmin.error import UserNotFoundError, UserFoundError, CouldNotQueryError
from pfAdmin.error import AliasFoundError, AliasNotFoundError
from pfAdmin.utils import Config, parse_email, connect_db


def encrypt_password(password):
    Co = Config()
    if Co.is_parsed() == False:
        Co.parse_config()
    config = Co.get_config()
    db = connect_db(config)
    c = db.cursor()
    str_query = """SELECT md5(%s)"""
    c.execute(str_query, (password, ))
    new_passes = c.fetchone()
    c.close()
    return new_passes[0]



class Mail(object):
    """docstring for Mail"""
    
    def __init__(self, path=''):
        
        self.__name__ = 'Mail'
        Co = Config()
        Co.set_path(path)
        if Co.is_parsed() == False:
            Co.parse_config()
        self.config = Co.get_config()
        self.db = connect_db(self.config)
        

    def list_domains(self):
        
        query = """SELECT %s FROM %s""" % (self.config['domains.name'], \
        self.config['domains'])
        c = self.db.cursor()
        c.execute(query)
        domains = []
        if c.rowcount > 0:
            domains = c.fetchall()
        c.close()
        return domains

    def add_domain(self, domain_name):
        
        dom = Domain(domain_name)
        if dom.is_created():
            raise DomainFoundError(domain_name)
        else:
            dom.create()
    
    def delete_domain(self, domain_name):
        
        dom = Domain(domain_name)
        if dom.is_created():
            dom.delete()
        else:
            raise DomainNotFoundError(domain_name)
            
    def list_aliases(self, source):
        
        ala = Alias(source)
        if ala.list_destination():
            return ala.list_destination()
        else:
            raise AliasNotFoundError(source)
        
    def add_alias(self, source, destination):
        usu = User(source, '')
        if not usu.is_created():
            raise UserNotFoundError(source)
        else:
            ala = Alias(source, destination)
            if not ala.is_created():            
                ala.create()
            else:
                raise AliasFoundError(source, destination)
        
    def delete_alias(self, source, destination):
        usu = User(source, '')
        if not usu.is_created():
            raise UserNotFoundError(source)
        else:
            ala = Alias(source, destination)
            if not ala.is_created():
                raise AliasNotFoundError(source, destination)
            else:
                ala.delete()
               
    def list_users(self, domain):
        
        dom = Domain(domain)
        if not dom.is_created():
            raise DomainNotFoundError(domain)
        else:
            return dom.list_users()
                        
    def add_user(self, username, password):
        
        user, domain = parse_email(username)
        dom = Domain(domain)
        if not dom.is_created():
            raise DomainNotFoundError(domain)
        else:
            usu = User(username, password)
            if not usu.is_created():
                usu.create()
            else:
                raise UserFoundError(username)

    def delete_user(self, username):
        
        user, domain = parse_email(username)
        usu = User(username)
        if not usu.is_created():
            raise UserNotFoundError(username)
        else:
            usu.delete()
                
    def update_password(self, username, password):
       
        usu = User(username)
        if not usu.is_created():
            raise UserNotFoundError(username)
        else:
            usu.update_password(password)

class Domain(object):

        
    def __init__(self, domain_name):
        
        self.domain_name = domain_name
        Co = Config()
        if Co.is_parsed() == False:
            Co.parse_config()
        self.config = Co.get_config()
        self.db = connect_db(self.config)
        
    
    def list_users(self):
       
        query = """SELECT %s, %s FROM %s AS vu JOIN %s AS vd on vu.%s=vd.%s \
        WHERE %s=""" % (self.config['users.user'], \
        self.config['domains.name'], self.config['users'], \
        self.config['domains'], self.config['users.domain_id'], \
        self.config['domains.id'], self.config['domains.name']) + """%s"""
        c = self.db.cursor()
        c.execute(query, (self.domain_name,))
        users = []
        if c.rowcount > 0:
            lists = c.fetchall()
            for element in lists:
                users.append(element[0] + '@' + element[1])
        c.close()
        return users

        
    def is_created(self):
        
        query = """SELECT %s FROM %s WHERE %s=""" % \
        (self.config['domains.name'], self.config['domains'], \
        self.config['domains.name']) + """%s"""
        c = self.db.cursor()
        c.execute(query, (self.domain_name,))
        if c.rowcount == 1:
            c.close()
            return True
        else:
            c.close()
            return False

    def create(self):

        c = self.db.cursor()
        str_query = """INSERT INTO %s (%s) """ % (self.config['domains'],\
        self.config['domains.name']) + """VALUES (%s)"""
        c.execute(str_query, (self.domain_name))
        if c.rowcount == 1:
            self.db.commit()
            c.close()
        else:
            self.db.rollback()
            c.close()
            raise CouldNotQueryError(str_query % domain_name)

    def delete(self):

        c = self.db.cursor()
        str_query = """DELETE FROM %s WHERE %s = """ % \
        (self.config['domains'], self.config['domains.name']) + """%s"""
        c.execute(str_query, (self.domain_name))
        if c.rowcount == 1:
            self.db.commit()
            c.close()   
        else:
            self.db.rollback()
            c.close()
            raise CouldNotQueryError(str_query % (self.domain_name))

    def get_name(self):
        return self.domain_name

class Alias(object):
    
    def __init__(self, source, destination=''):
            
            self.destination = destination
            self.name, self.domain = parse_email(source)
            Co = Config()
            if Co.is_parsed() == False:
                Co.parse_config()
            self.config = Co.get_config()
            self.db = connect_db(self.config)
        
    def list_destination(self):
        
        query = """SELECT %s FROM %s AS va JOIN %s AS vd on va.%s=vd.%s WHERE \
        %s""" % (self.config['aliases.destination'], self.config['aliases'], \
        self.config['domains'], self.config['aliases.domain_id'], \
        self.config['domains.id'], self.config['aliases.source']) + """=%s""" \
        + """ AND %s=""" % self.config['domains.name'] + """%s"""
        c = self.db.cursor()
        c.execute(query, (self.name, self.domain))
        aliases = []
        if c.rowcount > 0:
            lists = c.fetchall()
            for element in lists:
                aliases.append(element[0])
        c.close()
        return aliases
    
    def is_created(self):
        
        query = """SELECT * FROM %s AS va JOIN %s AS vd ON va.%s=vd.%s WHERE \
        %s""" % (self.config['aliases'], self.config['domains'], \
        self.config['aliases.domain_id'], self.config['domains.id'], \
        self.config['domains.name']) + """=%s AND """ + """%s=""" % \
        self.config['aliases.source']  + """%s AND """ + """%s=""" % \
        self.config['aliases.destination'] + """%s"""
        c = self.db.cursor()
        c.execute(query, (self.domain, self.name, self.destination,))
        if c.rowcount == 1:
            c.close()
            return True
        else:
            c.close()
            return False
    
    def create(self):
        
        query = """INSERT INTO %s (%s, %s, %s) VALUES(""" % \
        (self.config['aliases'], self.config['aliases.source'], \
        self.config['aliases.destination'], self.config['aliases.domain_id'])+\
        """%s, %s, """ + """(SELECT %s FROM %s WHERE %s=""" % \
        (self.config['domains.id'], self.config['domains'], \
        self.config['domains.name']) + """%s))"""
        c = self.db.cursor()
        c.execute(query, (self.name, self.destination, self.domain,))
        if c.rowcount == 1:
            self.db.commit()
            c.close()
        else:
            self.db.rollback()
            c.close()
            raise CouldNotQueryError(str_query % (self.name, \
            self.destination, self.domain))
    
    def delete(self):
        
        c = self.db.cursor()
        str_query = """DELETE FROM %s USING %s JOIN %s ON %s.%s=%s.%s WHERE \
        %s = """ % (self.config['aliases'], self.config['aliases'], \
        self.config['domains'], self.config['aliases'], \
        self.config['aliases.domain_id'], self.config['domains'], \
        self.config['domains.id'], self.config['aliases.source']) + """%s AND \
        """ + """%s = """ % self.config['domains.name'] + """%s""" + """ AND \
        %s=""" % self.config['aliases.destination'] + """%s"""
        c.execute(str_query, (self.name, self.domain, self.destination))
        if c.rowcount == 1:
            self.db.commit()
            c.close()
        else:
            self.db.rollback()
            c.close()
            raise CouldNotQueryError(str_query % (self.name, self.domain, \
            self.destination))

        
class User(object):
    """docstring for User"""

        
    def __init__(self, username, password=''):
        
        self.__name__ = username
        Co = Config()
        if Co.is_parsed() == False:
            Co.parse_config()
        self.config = Co.get_config()
        self.db = connect_db(self.config)
        self.user, self.domain = parse_email(username)
        self.password = password

    def is_created(self):
        
        query = """SELECT * FROM %s AS vu JOIN %s AS vd on vu.%s = vd.%s \
        WHERE %s =""" % (self.config['users'], self.config['domains'], \
        self.config['users.domain_id'], self.config['domains.id'], \
        self.config['users.user']) + """%s""" + """AND %s=""" % \
        (self.config['domains.name']) + """%s"""
        c = self.db.cursor()
        c.execute(query, (self.user, self.domain,))
        if c.rowcount == 1:
            c.close()
            return True
        else:
            c.close()
            return False

    def create(self):
        
        enc_pass = encrypt_password(self.password)
        c = self.db.cursor()
        str_query = """INSERT INTO %s""" % self.config['users'] + \
        """ (%s, %s, %s)""" % (self.config['users.domain_id'], \
        self.config['users.user'], self.config['users.password']) + \
        ' VALUES ((SELECT %s AS %s FROM %s WHERE %s=' % \
        (self.config['domains.id'], self.config['users.domain_id'], \
        self.config['domains'], self.config['domains.name'])+ '%s), %s, %s)'
        c.execute(str_query, (self.domain, self.user, enc_pass, ))
        if c.rowcount == 1:
            self.db.commit()
            c.close()
        else:
            self.db.rollback()
            c.close()
            raise CouldNotQueryError(str_query % (self.domain, \
            self.user, self.password))

    def update_password(self, new_pass):
        """docstring for update_password"""

        enc_pass = encrypt_password(new_pass)
        c = self.db.cursor()
        str_query = """UPDATE %s AS vu JOIN %s as vd on vu.%s = vd.%s SET %s \
        = """ % (self.config['users'], self.config['domains'], \
        self.config['users.domain_id'], self.config['domains.id'], \
        self.config['users.password']) + """%s""" + """ WHERE %s = """ % \
        self.config['users.user'] + """%s"""+ """ AND %s = """ % \
        self.config['domains.name'] + """%s"""
        c.execute(str_query, (enc_pass, self.user, self.domain))
        if c.rowcount == 1:
            self.db.commit()
            self.password = enc_pass
            c.close()
        else:
            self.db.rollback()
            c.close()
            raise CouldNotQueryError(str_query % (new_pass, self.user, \
            self.domain))

    def delete(self):

        c = self.db.cursor()
        str_query = """DELETE FROM %s USING %s JOIN %s ON %s.%s=%s.%s WHERE \
        %s = """ % (self.config['users'], self.config['users'], \
        self.config['domains'], self.config['users'], \
        self.config['users.domain_id'], self.config['domains'], \
        self.config['domains.id'], self.config['users.user']) + """%s AND \
        """ + """%s = """ % self.config['domains.name'] + """%s"""
        c.execute(str_query, (self.user, self.domain,))
        if c.rowcount == 1:
            self.db.commit()
            c.close()
        else:
            self.db.rollback()
            c.close()
            raise CouldNotQueryError(str_query % (self.user, self.domain,))

    def get_name(self):
        """docstring for get_name"""
        
        return self.user

    def get_password(self):

        return self.password




def test_main():
    """docstring for __main__"""


    

if __name__ == '__main__':
    test_main()
