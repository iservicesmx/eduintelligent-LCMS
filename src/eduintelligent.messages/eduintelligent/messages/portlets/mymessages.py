"""Define a portlet used to show the current user's courses. This follows the 
patterns from plone.app.portlets.portlets. Note that we also need a 
portlet.xml in the GenericSetup extension profile to tell Plone about our 
new portlet.
"""
from zope.interface import Interface
from zope.component import getMultiAdapter
from zope.interface import implements
from zope.component import getUtility

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Acquisition import aq_parent, aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot

from eduintelligent.messages import messagesMessageFactory as _
from eduintelligent.messages.interfaces import IMessagesManager


# This interface defines the configurable options (if any) for the portlet.
# It will be used to generate add and edit forms. In this case, we don't
# have an edit form, since there are no editable options.
class IMyMessages(Interface):
    """A box displaying "my course tools"
    """
    pass

# The assignment is a persistent object used to store the configuration of
# a particular instantiation of the portlet.
class Assignment(base.Assignment):
    implements(IMyMessages)

    @property
    def title(self):
        return _(u"My Messages")

# The renderer is like a view (in fact, like a content provider/viewlet). The
# item self.data will typically be the assignment (although it is possible
# that the assignment chooses to return a different object - see 
# base.Assignment).

class Renderer(base.Renderer):

    implements(IMyMessages)

    # render() will be called to render the portlet
    
    render = ViewPageTemplateFile('mymessages.pt')
       
    # The 'available' property is used to determine if the portlet should
    # be shown.
        
    @property
    def available(self):
        context = aq_inner(self.context)
        if ISiteRoot.providedBy(context):
            return True
        return False

    # By using the @memoize decorator, the return value of the function will
    # be cached. Thus, calling it again does not result in another query.
    # See the plone.memoize package for more.
                
    @memoize
    def categories(self):
        mtool = getToolByName(self.context, 'portal_membership')
        member = mtool.getAuthenticatedMember().getId()
        manager = getUtility(IMessagesManager)
        categories = manager.messages_categories(member)
        return categories
        
        

# Define an add view - by using NullAddForm, we signal that we don't want
# a visible form, since there are no options to set anyway.

class AddForm(base.NullAddForm):
    
    # This method must be implemented to actually construct the object.

    def create(self):
        return Assignment()
