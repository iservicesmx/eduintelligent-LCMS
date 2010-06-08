from zope.interface import implements
from persistent import Persistent
    
from zope.interface import implements
from zope.component import getUtility

from collective.lead import Database

from sqlalchemy.engine.url import URL
from sqlalchemy import Table
from sqlalchemy.orm import mapper, relation

from eduintelligent.messages.dbclasses import Messages, MessagesCategory
from eduintelligent.loginhistory.dbclasses import LoginHistory


from eduintelligent.database.interfaces import IDatabaseSettings

class EduIntelligentDatabaseSettings(Persistent):
    """Database connection settings
    
    We use raw fields here so that we can more easily use a zope.formlib
    form in the control panel to configure it. This is registered as a
    persistent local utility, with name 'optilux.reservations', which is
    then used by collective.lead.interfaces.IDatabase to find connection settings.
    """
    
    implements(IDatabaseSettings)
    
    drivername = 'postgres'
    hostname = 'localhost'
    port = None
    username = 'postgres'
    password = None
    database = 'tests'


class EduIntelligentDatabase(Database):
    """The reservations database - registered as a utility providing
    collective.lead.interfaces.IDatabase and named 'eduintelligent.db'
    """

    @property
    def _url(self):
        settings = getUtility(IDatabaseSettings)
        return URL(drivername=settings.drivername, username=settings.username,
                   password=settings.password, host=settings.hostname,
                   port=settings.port, database=settings.database)

    def _setup_tables(self, metadata, tables):
        """Map the database structure to SQLAlchemy Table objects
        """
        tables['messages'] = Table('messages', metadata, autoload=True)
        tables['messagescategory'] = Table('messagescategory', metadata, autoload=True)
        tables['loginhistory'] = Table('loginhistory', metadata, autoload=True)
    # 
    def _setup_mappers(self, tables, mappers):
        """Map the database Tables to SQLAlchemy Mapper objects
        """        
        mappers['messagescategory'] = mapper(MessagesCategory, tables['messagescategory'])
        
        mappers['messages'] = mapper(Messages, tables['messages'],)
                                        # properties = {
                                        #     'category' : relation(MessagesCategory),
                                        #     })
        mappers['loginhistory'] = mapper(LoginHistory, tables['loginhistory'])
        