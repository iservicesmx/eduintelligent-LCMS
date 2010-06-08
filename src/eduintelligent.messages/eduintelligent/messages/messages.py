from datetime import datetime

from zope.interface import implements
from zope.component import getUtility
from zope.app.component.hooks import getSite

from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName

from eduintelligent.messages.interfaces import IMessagesManager
from eduintelligent.messages.dbclasses import MessagesCategory, Messages

from sqlalchemy import *
from collective.lead.interfaces import IDatabase

__docformat__="reStructuredText"

class MessagesManager(object):
    """
    """
    implements(IMessagesManager)

    @property
    def _database(self):
        db = getUtility(IDatabase, name='eduintelligent.db')
        return db

    @property
    def _session(self):
        return self._database.session
    
    def message_by_id(self, message_id, read_flag):
        """Get a IMessages from a screening id
        """
        message = self._session.query(Messages).get(message_id)
        if read_flag:
            message.read_flag = True
            self._session.save_or_update(message)
            self._session.flush()
        return message
        
        
    def message_new(self, category_id, sender, receiver, subject, body, senddate=None, read_flag=False):
        """Create a New Message
        @param category_id : Store the message on this category.
        @param sender: User whom sends the message
        @param receiver: User whom recives the message
        @param subject: message subject
        @param body: message body
        @param sendDate: It is allways now() it should be deleted from the param list!!
        @param read_flag: It is always false. 
        
        TODO: review the relevance of the parameters sendDate and read_flag.
        """
        senddate = datetime.now()
        message = Messages(category_id, sender, receiver, subject, body, senddate, read_flag)
        self._session.save(message)
        self._session.flush()
        
    def message_delete(self, message_id):
        """Delete the message identified by message_id
        """
        message = self._session.query(Messages).get(message_id)
        self._session.delete(message)
        self._session.flush()
        
    def message_flag(self, message_id):
        """Flags the message idenfied by message_id as 'read'
        """
        message = self._session.query(Messages).get(message_id)
        message.read_flag = 1
        self._session.save_or_update(message)
        self._session.flush()
        
    def message_move(self, message_id, cat_id):
        """Moves the message identified by message_id to the category cat_id
        """
        category = self._session.query(MessagesCategory).get(cat_id)
        message = self._session.query(Messages).get(message_id)
        message.category_id = category
        self._session.save_or_update(message)
        self._session.flush()
        
    def messages_category_user(self, cat_id, user_id):
        """ Returns all the messages in category cat_id that were 
        sent to user_id. All messages sorted by date sent and in
        descendant order.
        """        
        # messages = self._session.query(Messages).filter_by(id=cat_id).\
        #                         reset_joinpoint().filter_by(receiver=user_id).all()
        # return messages
        messages = self._session.query(Messages).filter(and_(Messages.category_id==cat_id,Messages.receiver==user_id)).order_by(Messages.senddate.desc())
        return messages.all()
        
    def messages_count(self, cat_id, user_id):
        """ Count all messages sent to user_id in the given category
        cat_id.
        TODO: It does nothing now!! We should consider removing it
        """
        pass        
        # Count all message from user
        #total = self._session.query(Messages).filter_by(Messages.category_id=cat_id, receiver=user_id).count()
        # Count only unflag messages user
        #unread = self._session.query(Messages).filter_by(Messages.category_id=cat_id, receiver=user_id, read_flag=False).count()
        
        #return (total, unread)
    
    def messages_categories(self, user_id):
        """Returns a dict that contains:
        id = Category id
        title = Category Name
        total = Total messages in this category
        unread = Unread messages in this category
        
        TODO: we should remove messages_count(). It does nothing!!
        """
        category = self._session.query(MessagesCategory).order_by(MessagesCategory.display_order)
        return [dict(id=cat.id,
                     title=cat.name,
                     total=self._session.query(Messages).filter(and_(Messages.category_id==cat.id, Messages.receiver==user_id)).count(),
                     unread=self._session.query(Messages).filter(and_(Messages.category_id==cat.id, Messages.receiver==user_id, Messages.read_flag==False)).count())
                for cat in category.all()]
        