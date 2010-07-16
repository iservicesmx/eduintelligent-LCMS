from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from AccessControl import getSecurityManager, Unauthorized
from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ModifyPortalContent
from Products.statusmessages.interfaces import IStatusMessage

from eduintelligent.courses.interfaces import ICourse
from plone.memoize.instance import memoize

class CourseInfo(BrowserView):
    """
    """
    
    @memoize
    def getCourses(self):
        """
        Nota: revizar que es lo mas optimo, si generar previamente un diccionario con los datos o desde la plantilla
            obtener los datos del objeto
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        
        contents = [b.getObject() for b in catalog(object_provides=ICourse.__identifier__,
                                            path=dict(query='/'.join(context.getPhysicalPath()),),
                                            sort_on='sortable_title')
                    ]
        
        #print contents
        
        return [ dict(url=course.absolute_url(),
                      id=course.getId(),
                      title=course.Title,
                      category=course.getCourseCategory(),
                      state=course.getPublishState(),
                      enrolled=course.getRegistered(),
                      instructor=course.getInstructor(),
                      start=course.start(),
                      end=course.end(),)
                      for course in contents]
        
    def getStateCourseReport(self):
        publish=0
        pending=0
        draft=0
        for course in self.getCourses():
            if course['state'] == 'published':
                publish += 1
            elif course['state'] == 'pending':
                pending += 1
            else:
                draft +=1
        return (publish, pending, draft)
        
    def getNumCecapCategories(self):
        return len(self.context._getOb('courses').getCategories())
        
