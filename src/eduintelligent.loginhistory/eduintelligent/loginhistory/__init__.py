"""Main product initializer
"""
#
from zope.i18nmessageid import MessageFactory

loginhistoryMessageFactory = MessageFactory('eduintelligent.loginhistory')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    pass
