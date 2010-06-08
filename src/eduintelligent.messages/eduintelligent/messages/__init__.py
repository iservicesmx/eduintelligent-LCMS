"""Main product initializer
"""

import logging

from zope.i18nmessageid import MessageFactory
from eduintelligent.messages import config

from Products.Archetypes import atapi
from Products.CMFCore import utils
from Products.CMFCore.permissions import setDefaultRoles

# Define a message factory for when this product is internationalised.
# This will be imported with the special name "_" in most modules. Strings
# like _(u"message") will then be extracted by i18n tools for translation.

messagesMessageFactory = MessageFactory('eduintelligent.messages')


logger = logging.getLogger('eduintelligent.messages')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    pass           

