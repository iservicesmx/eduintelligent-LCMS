"""Main product initializer
"""

from zope.i18nmessageid import MessageFactory

#from Products.CMFCore.permissions import setDefaultRoles
zipcontentMessageFactory = MessageFactory('eduintelligent.zipcontent')

#setDefaultRoles("ediIntelligent: Add ZIP", ('Manager',))

def initialize(context):
    """Intializer called when used as a Zope 2 product."""    
    pass
    