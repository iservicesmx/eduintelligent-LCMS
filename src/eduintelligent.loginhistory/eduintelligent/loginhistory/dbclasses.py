from sqlalchemy import *

# Create connection
#engine = create_engine('sqlite:///Users/erik/Desarrollo/cecade/var/mydb.db', echo=True)
engine = create_engine('postgres://zope:zope@localhost/darier_logs', echo=True)

# Define tebles
metadata = MetaData()
loginhistory_table = Table('loginhistory', metadata,
                Column('id', Integer, primary_key=True),
                Column('username', String(255)),
                Column('startdate', DateTime),
                Column('enddate', DateTime),
                Column('sessionid', String(255)),
                Column('browser', String(255)),
                Column('ip', String(255)),
                Column('usergroup', String(255)),
                Column('success', Boolean),
                )

class LoginHistory(object):
    def __init__(self, username, startdate, enddate, sessionid, usergroup, ip, browser, success):
        self.username    = username
        self.startdate   = startdate
        self.enddate     = enddate
        self.sessionid   = sessionid
        self.usergroup   = usergroup
        self.ip          = ip
        self.browser     = browser
        self.success     = success

    def __repr__(self):
        return "<LoginHistory ('%s','%s')>" % (self.username, self.startdate)

if __name__=='__main__':
    #drop tables
    #metadata.drop_all(engine)

    # Create table if doesn't exist
    metadata.create_all(engine)
