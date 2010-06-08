# -*- coding: utf-8 -*-
"""Define a portlet used to show courses. This follows the patterns from
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

from eduintelligent.courses.interfaces import ICourse
from eduintelligent.courses import coursesMessageFactory as _


# This interface defines the configurable options (if any) for the portlet.
# It will be used to generate add and edit forms.

class ICoursesPortlet(IPortletDataProvider):

    count = schema.Int(title=_(u'Number of courses to display'),
                       description=_(u'Maximum number of courses to be shown'),
                       required=True,
                       default=5)
                       
    randomize = schema.Bool(title=_(u'Randomize courses'),
                            description=_(u'If enabled, courses to show will be picked randomly.'),
                            default=False)
                            

# The assignment is a persistent object used to store the configuration of
# a particular instantiation of the portlet.

class Assignment(base.Assignment):
    implements(ICoursesPortlet)

    def __init__(self, count=5, randomize=False):
        self.count = count
        self.randomize = randomize

    @property
    def title(self):
        return _(u'My Courses')

# The renderer is like a view (in fact, like a content provider/viewlet). The
# item self.data will typically be the assignment (although it is possible
# that the assignment chooses to return a different object - see 
# base.Assignment).

class Renderer(base.Renderer):

    # render() will be called to render the portlet
    
    render = ViewPageTemplateFile('mycourses.pt')
       
    # The 'available' property is used to determine if the portlet should
    # be shown.
        
    #@property
    #def available(self):
    #    return len(self._data()) > 0
    
    def all_courses(self):
        context = aq_inner(self.context)
        
        portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        
        portal_url = portal_state.portal_url()                                    
        
        membership = getToolByName(context, 'portal_membership')
        member = membership.getAuthenticatedMember()
        main_group = member.getProperty('main_group', 'manager')
        return portal_url + '/' + main_group + '/courses'

    # To make the view template as simple as possible, we return dicts with
    # only the necessary information.

    def courses(self):
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
        
        query = dict(object_provides = ICourse.__identifier__)
        
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
        
        courses = []
        if self.data.randomize:
            courses = list(results)
            courses.sort(lambda x,y: cmp(random.randint(0,200),100))
            courses = courses[:limit]
        else:
            courses = results[:limit]
        
        return courses

# Define the add forms and edit forms, based on zope.formlib. These use
# the interface to determine which fields to render.

class AddForm(base.AddForm):
    form_fields = form.Fields(ICoursesPortlet)
    label = _(u'Add Course portlet')
    description = _(u'This portlet displays my courses.')

    # This method must be implemented to actually construct the object.
    # The 'data' parameter is a dictionary, containing the values entered
    # by the user.

    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment

class EditForm(base.EditForm):
    form_fields = form.Fields(ICoursesPortlet)
    label = _(u'Edit Courses portlet')
    description = _(u'This portlet displays my courses.')
