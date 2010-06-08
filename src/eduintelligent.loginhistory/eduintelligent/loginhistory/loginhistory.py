from zope.interface import implements
from zope.component import getUtility
from zope.app.component.hooks import getSite

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import security

from eduintelligent.loginhistory.interfaces import ILoginHistoryManager
from eduintelligent.loginhistory.interfaces import ILoginHistory
from eduintelligent.loginhistory.dbclasses import LoginHistory

from sqlalchemy import *
from sqlalchemy.sql import func

from collective.lead.interfaces import IDatabase

from datetime import datetime, timedelta

class LoginHistoryManager(object):
    """
    """
    implements(ILoginHistoryManager)
    
    @property
    def _database(self):
        db = getUtility(IDatabase, name='eduintelligent.db')
        db.session
        return db

    @property
    def _session(self):
        return self._database.session

    @property
    def _connection(self):
        return self._database.connection

        
    def login_in(self, userid, ip, browser, session, group):
        """Create a New Login History
        """        
        lh = LoginHistory(username=userid, 
                        startdate=datetime.now(), 
                        enddate=datetime.now() + timedelta(minutes=1), 
                        sessionid=session, 
                        usergroup=group, 
                        ip=ip, 
                        browser=browser[:254], 
                        success=False)
        self._session.save(lh)
        self._session.flush()
        
    def login_out(self, user, session):
        lh = self._session.query(LoginHistory).filter_by(username=user,sessionid=session).all()
        if len(lh):
            lh = lh[-1]
            lh.enddate=datetime.now()
            lh.success=True
            self._session.save_or_update(lh)
            self._session.flush()
        

    def login_by_id(self, login_id):
        """Get an LoginHistory by id
        """
        lg = self._session.query(LoginHistory).get(login_id)
        
        return lg
        
    def login_all(self):
        """
        """
        lgs = self._session.query(LoginHistory).order_by(LoginHistory.startdate.desc()).limit(300)
        return lgs.all()

    def login_by_user(self, username, startdate, enddate):
        """
        """
        lh = self._session.query(LoginHistory).filter(and_(LoginHistory.username==username, LoginHistory.startdate.between(startdate, enddate))).order_by(LoginHistory.c.startdate.desc())
        return lh.all()


    def login_by_group_complete(self, group, startdate, enddate, user=None):
        """
        """
        lh = self._session.query(LoginHistory).filter(and_(LoginHistory.usergroup==group, LoginHistory.startdate.between(startdate, enddate))).order_by(LoginHistory.c.startdate.desc())
        return lh.all() 
        
    def login_by_group_grouped(self, group, startdate, enddate):
        #lh = self._session.query(LoginHistory)
        #r = ("SELECT username, MAX(startdate) as total, COUNT(*) FROM loginhistory WHERE usergroup=:usergroup AND startdate >= :startdate AND startdate <=:enddate GROUP BY username ORDER BY total DESC",{'usergroup':group,'startdate':startdate,'enddate':enddate})
        #return lh.execute("SELECT username, MAX(startdate) as total, COUNT(*) FROM loginhistory WHERE usergroup=:usergroup AND startdate >= :startdate AND startdate <=:enddate GROUP BY username ORDER BY total DESC",{'usergroup':group,'startdate':startdate,'enddate':enddate})
        
        # lh = self._session.query(LoginHistory).filter(and_(LoginHistory.usergroup==group, LoginHistory.startdate.between(startdate, enddate))).group_by([LoginHistory.c.username]).order_by(LoginHistory.c.startdate.desc()).add_column(func.count(LoginHistory.username).label('count'))
        # return lh.all()
        
        # lh = self._session.query(LoginHistory)
        # s = select([LoginHistory.c.username,func.max(LoginHistory.c.startdate).label('startdate'),func.count('*').label('total')],
        #     and_(LoginHistory.c.usergroup==group, LoginHistory.c.startdate.between(startdate, enddate)),).group_by(LoginHistory.c.username).order_by(LoginHistory.c.startdate.desc())
        # return lh.execute(s).fetchall()

        # lh = self._session.query(LoginHistory)
        # lh.select([LoginHistory.c.username,func.max(LoginHistory.c.startdate),func.count(LoginHistory.c.id)],and_(LoginHistory.c.usergroup==group, LoginHistory.c.startdate.between(startdate, enddate)),group_by=[LoginHistory.c.username], order_by=[LoginHistory.c.startdate.desc()])
        # return lh.all()
        
        # lh = self._session.query(LoginHistory).from_statement("SELECT username, MAX(startdate) as total, COUNT(*) FROM loginhistory WHERE usergroup=:usergroup AND startdate >= :startdate AND startdate <=:enddate GROUP BY username ORDER BY total DESC").params(usergroup=group,startdate=startdate,enddate=enddate).all()
        # return lh

        # statement = select([LoginHistory.username],
        #                        and_(
        #                             LoginHistory.usergroup==group,
        #                             LoginHistory.startdate.between(startdate, enddate)
        #                        ),
        #                        distinct=True)
        # 
        # results = self._session.query(LoginHistory).execute(statement).fetchall()
        # return results
        
        lh = self._session.query(LoginHistory).filter(and_(LoginHistory.usergroup==group, LoginHistory.startdate.between(startdate, enddate))).order_by(LoginHistory.c.startdate.desc())
        return lh.all() 
        

    def login_user_search(self, term):
        """
        """
        pass

security.declarePublic('getLH')
def getLH():
    return getUtility(ILoginHistoryManager)