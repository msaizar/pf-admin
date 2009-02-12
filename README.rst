pf-admin
========

about::

    pf-admin is one of my tools to manage my mail servers. 
    pf-admin.py manages the postfix/mysql database, use --help or -h for details.
    it is based on http://workaround.org/articles/ispmail-etch/ . this means it uses innodb, and when a domain is deleted, mysql takes care of deleting every user/alias too.

usage::

    see pf-admin.py -h or pf-admin.py --help for details
    

new in 0.2.0
============

- renamed project to pf-admin
- initial aliases support
- renamed main binary to pf-admin.py
- postfix admin will be the only tool as of now, may add other tools in a nearby future on separate repositories.

new in 0.1.0
============

- remade structure, more reusable and OO
- removed some unnecessary sub queries
- optimized load time
- added singleton classes for configuration/database management
- exceptions added to main library
- added new arguments, --list-users and --list-domains
- added a doc/sample.conf
- removed doc/dump.sql and doc/queries.rst
- final version of dependencies.rst
- moved main binary to root directory, removed /bin


new in 0.0.3
============

- main binary finished, bin/postfix-admin.py

new in 0.0.2
============

- renamed to adminsh
- created adminsh/error.py
- created temporary doc/dump.sql, for internal testing purposes
- moved docs to doc
- finished back-end. missing test unit

new in 0.0.1
============

- created docs/dependencies.rst
- created admin/mail.py with Mail, User, Domain classes
- created admin/utils.py with default configuration, retrieve configuration functions
- created docs/queries.rst with some query ideas
- created directory structure
- created README.rst