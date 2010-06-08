"""
$Id$
"""

__author__ = """Erik Rivera Morales <erik@ro75.com>"""
__docformat__ = 'plaintext'
__licence__ = 'GPL'

from zope.component import getUtility
from Acquisition import aq_base, aq_parent

from eduintelligent.loginhistory.interfaces import ILoginHistoryManager

def userLoggedIn(obj, event):
    pas = aq_parent(obj)
    REQUEST = pas.REQUEST
    
    userid = obj.getId()
    user    = REQUEST['AUTHENTICATED_USER']
    browser = REQUEST['HTTP_USER_AGENT']
    ip      = REQUEST['REMOTE_ADDR'] #if unpatched VirtualHostMonster used REMOTE_ADDR is always the local proxy
    session = REQUEST['SESSION'].token
    #print "Entrada"
    #print "userid",userid
    #print "sesToken",session
    
    group = user.getProperty('main_group','manager')

    if ip == '127.0.0.1':
        ip = REQUEST['HTTP_X_FORWARDED_FOR']
    
    lh = getUtility(ILoginHistoryManager)        
    lh.login_in(userid,ip,browser,session,group)
    
def userLoggedOut(obj, event):
    pas = aq_parent(obj)
    REQUEST = pas.REQUEST
    session = REQUEST['SESSION'].token
    userid = obj.getId()
    
    lh = getUtility(ILoginHistoryManager)        
    lh.login_out(userid, session)
    
    #print "Salida"
    #print "userid",userid    
    #print "sesTO",session
    