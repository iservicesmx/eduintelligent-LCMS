"""Main product initializer
"""

from zope.i18nmessageid import MessageFactory

from Products.CMFCore.permissions import setDefaultRoles
scoMessageFactory = MessageFactory('eduintelligent.sco')

setDefaultRoles("ediIntelligent: Add SCO", ('Manager',))

def initialize(context):
    """Intializer called when used as a Zope 2 product."""    
    pass
    