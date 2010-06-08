from zope.interface import Interface
from zope import schema

#from zope.app.container.constraints import contains
#from zope.app.container.constraints import container

from eduintelligent.messages import messagesMessageFactory as _

class IMessagesCategory(Interface):
    """Messages Categories like Inbox, Sent, Trash
    """
    category_id = schema.Int(title=_(u"Category identifier"),
                              description=_(u"A unique id for this category"),
                              required=True,
                              readonly=True)
                              
    display_order = schema.Int(title=_(u"Category Order"),
                            description=_(u"The order in a list of categories"),
                            required=True)
                            
    name =          schema.TextLine(title=_(u"Name"),
                            description=_(u"The category name"))

class IMessages(Interface):
    """Messages
    """
    message_id = schema.Int(title=_(u"Message identifier"),
                              description=_(u"A unique id for this message"),
                              required=True,
                              readonly=True)
                              
    category_id = schema.Int(title=_(u"Category Id"),
                            description=_(u"the category id belong"),
                            required=True)
                            
    read_flag = schema.Int(title=_(u"Read Flag"),
                            description=_(u"True if is readed"),)
                            
    sender = schema.TextLine(title=_(u"From"),
                            description=_(u"User whom sends the message"))
                            
    receivier = schema.TextLine(title=_(u"To"),
                            description=_(u"User whom recives the message"))
                            
    subject = schema.TextLine(title=_(u"Subject"),)
    
    body = schema.SourceText(title=_(u"Message text"),)
    
    creation_date =      schema.Date(title=_(u"Creation date"),)
                            
class IMessagesManager(Interface):
    """Messages Categories like Inbox, Sent, Trash
    """
    def message_by_id(message_id):
        """Get an IMessages from a screening id
        
        message1 = session.query(Messages).get(message_id)
        
        """
        
    def message_new(category_id, sender, receivier, subject, text, read_flag=0):
        """Create a New Message
        
        category = session.query(MessagesCategory).get(category_id)
        message = Messages(category, sender, receivier, subject, text, read_flag)
        
        """
    def message_delete(message_id):
        """
        message1 = session.query(Messages).get(message_id)
        session.delete(message1)
        
        """
    def message_flag(message_id):
        """
        message1 = session.query(Messages).get(message_id)
        message1.read_flag = 1
        session.update(message1)
        """
    def message_move(message_id, cat_id):
        """
        category = session.query(MessagesCategory).get(cat_id)
        message1 = session.query(Messages).get(message_id)
        message1.cat_id = category
        session.update(message1)
        """
                
    def messages_category_user(category_id, user_id):
        """
        session.query(Messages).join('messages_category').\
        ...     filter_by(category_id=1).\
        ...     reset_joinpoint().filter_by(receiver='erik1234').all()
        
        """

        
    def messages_count(cat_id, user_id):
        """
        # Count all message from user
        session.query(Messages).join('messages_category').\
        ...     filter_by(category_id=cat_id).\
        ...     reset_joinpoint().filter_by(receiver=user_id).count()
        
        # Count only unflag messages user
        session.query(Messages).join('messages_category').\
        ...     filter_by(category_id=cat_id).\
        ...     reset_joinpoint().filter_by(receiver=user_id, read_flag=0).count()
        
        
        """