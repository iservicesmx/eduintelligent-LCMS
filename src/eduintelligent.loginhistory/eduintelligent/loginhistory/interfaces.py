from zope.interface import Interface
from zope import schema

from eduintelligent.loginhistory import loginhistoryMessageFactory as _

class ILoginHistory(Interface):
    """Login History
    """
                            
class ILoginHistoryManager(Interface):
    """Messages Categories like Inbox, Sent, Trash
    """
    def new_login(args):
        """
        """
        
    def login_by_id(login_id):
        """        
        """
        
    def login_by_user(userid):
        """
        """
        
    def login_by_cecap(cecap):
        """
        """
        
    def login_user_search(term):
        """
        """
