class Error(Exception):
    pass


class CouldNotQueryError(Error):
    """docstring for CouldNotInsertError"""
    pass


class UserNotFoundError(Error):
    """docstring for UserNotFoundError"""

    pass

class ConfigNotFoundError(Error):
    pass

class AliasFoundError(Error):
    pass
    
class AliasNotFoundError(Error):
    pass
    
class UserFoundError(Error):

    """docstring for UserFoundError"""

    pass
    
class InvalidUsernameFormatError(Error):
    pass

class DomainNotFoundError(Error):
    """docstring for DomainNotFoundError"""
    pass


class DomainFoundError(Error):
    """docstring for DomainFoundError"""
    pass
