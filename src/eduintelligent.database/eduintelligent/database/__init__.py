#
from zope.i18nmessageid import MessageFactory

databaseMessageFactory = MessageFactory('eduintelligent.database')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
