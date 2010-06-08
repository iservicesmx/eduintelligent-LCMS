from sqlalchemy import *

# Create connection
#engine = create_engine('sqlite:///Users/erik/Desarrollo/cecade/var/mydb.db', echo=True)
engine = create_engine('postgres://zope:zope@localhost/darier_logs', echo=True)

# Define tebles
metadata = MetaData()

messagescategory_table = Table('messagescategory', metadata,
                Column('id', Integer, primary_key=True),
                Column('display_order', Integer),
                Column('name', String(50)),
                )
messages_table = Table('messages', metadata,
                Column('id', Integer, primary_key=True),
                Column('subject', String(255)),
                Column('body', String),
                Column('senddate', DateTime),
                Column('receiver', String(255)),
                Column('sender', String(255)),
                Column('read_flag', Boolean),
                Column('files', String),
                Column('category_id', Integer, ForeignKey('messagescategory.id')),
                )
        
class MessagesCategory(object):
    """Messages Categories like Inbox, Sent, Trash
    """
    #implements(IMessages)
    display_order = None
    name = None
    
    def __init__(self, display_order, name):
        self.display_order = display_order
        self.name  = name
        
    def __repr__(self):
        return "<MessagesCategory ('%s','%s')>" % (self.display_order, self.name)

class Messages(object):
    """A screening of a film at a particular cinema
    """
    #implements(IMessages)
    category_id = None
    read_flag = None
    sender = None
    receiver =  None
    subject = None
    body = None
    senddate = None

    def __init__(self, category_id, sender, receiver, subject, body, senddate, read_flag):
        self.category_id= category_id
        self.read_flag  = read_flag
        self.sender     = sender
        self.receiver   = receiver
        self.subject    = subject
        self.body       = body
        self.senddate   = senddate

    def __repr__(self):
        return "<Messages ('%s','%s')>" % (self.sender, self.subject)

if __name__=='__main__':
    #drop tables
    metadata.drop_all(engine)

    # Create table if doesn't exist
    metadata.create_all(engine)
