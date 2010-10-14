"""
$Id$
"""

__author__ = """Erik Rivera Morales <erik@iservices.mx>"""
__docformat__ = 'plaintext'
__licence__ = 'GPL'

from zope.component import getUtility
from Acquisition import aq_base, aq_parent
from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite

from eduintelligent.loginhistory.interfaces import ILoginHistoryManager


class checkProductInstalled(object):
    """
    Utility function that checks if this product is installed
    Would be nice if this was a decorator
    """
    def __init__(self,f):
        self.f = f

    def __call__(self,obj,event):
        """Class decorators need to be callable
        """
        portal = getSite()
        installer = getToolByName(portal,'portal_quickinstaller')
        installed_products = installer.keys()
        if 'eduintelligent.loginhistory' in installed_products:
            f()

@checkProductInstalled
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

@checkProductInstalled
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
    
