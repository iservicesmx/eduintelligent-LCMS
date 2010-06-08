"""Define a portlet used to show exams. This follows the patterns from
plone.app.portlets.portlets. Note that we also need a portlet.xml in the
GenericSetup extension profile to tell Plone about our new portlet.
"""

import random

from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from DateTime import DateTime
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from eduintelligent.evaluation.interfaces import IExam
from eduintelligent.evaluation import evaluationMessageFactory as _


# This interface defines the configurable options (if any) for the portlet.
# It will be used to generate add and edit forms.

class IExamsPortlet(IPortletDataProvider):

    count = schema.Int(title=_(u'Number of exams to display'),
                       description=_(u'Maximum number of exams to be shown'),
                       required=True,
                       default=5)
                       
    randomize = schema.Bool(title=_(u"Randomize exams"),
                            description=_(u"If enabled, exams to show will be picked randomly. "
                                            "If disabled, newer courses will be preferred."),
                            default=False)
                            

# The assignment is a persistent object used to store the configuration of
# a particular instantiation of the portlet.

class Assignment(base.Assignment):
    implements(IExamsPortlet)

    def __init__(self, count=5, randomize=False):
        self.count = count
        self.randomize = randomize

    @property
    def title(self):
        return _(u"My Exams")

# The renderer is like a view (in fact, like a content provider/viewlet). The
# item self.data will typically be the assignment (although it is possible
# that the assignment chooses to return a different object - see 
# base.Assignment).

class Renderer(base.Renderer):

    # render() will be called to render the portlet
    
    render = ViewPageTemplateFile('myexams.pt')
       
    # The 'available' property is used to determine if the portlet should
    # be shown.
        
    @property
    def available(self):
        return len(self._data()) > 0

    # To make the view template as simple as possible, we return dicts with
    # only the necessary information.

    def exams(self):
        for brain in self._data():
            #courses = brain.getObject()
            yield dict(title=brain.Title,
                       description=brain.Description,
                       url=brain.getURL())
        
    # By using the @memoize decorator, the return value of the function will
    # be cached. Thus, calling it again does not result in another query.
    # See the plone.memoize package for more.
        
    @memoize
    def _data(self):
        context = aq_inner(self.context)
        limit = self.data.count
        
        query = dict(object_provides = IExam.__identifier__)
        
        # if not self.data.sitewide:
        #     query['path'] = '/'.join(context.getPhysicalPath())
        if not self.data.randomize:
            query['sort_on'] = 'modified'
            query['sort_order'] = 'reverse'
            query['sort_limit'] = limit
        
        # Ensure that we only get active objects, even if the user would
        # normally have the rights to view inactive objects (as an
        # administrator would)
        query['effectiveRange'] = DateTime()
        
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(query)
        
        exams = []
        if self.data.randomize:
            exams = list(results)
            exams.sort(lambda x,y: cmp(random.randint(0,200),100))
            exams = exams[:limit]
        else:
            exams = results[:limit]
        
        return exams

# Define the add forms and edit forms, based on zope.formlib. These use
# the interface to determine which fields to render.

class AddForm(base.AddForm):
    form_fields = form.Fields(IExamsPortlet)
    label = _(u"Add Exam portlet")
    description = _(u"This portlet displays my exams.")

    # This method must be implemented to actually construct the object.
    # The 'data' parameter is a dictionary, containing the values entered
    # by the user.

    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment

class EditForm(base.EditForm):
    form_fields = form.Fields(IExamsPortlet)
    label = _(u"Edit exams portlet")
    description = _(u"This portlet displays my exams.")
