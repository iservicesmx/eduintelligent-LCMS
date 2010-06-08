from zope.interface import implements
#from plone.app.workflow.interfaces import ISharingPageRole
from eduintelligent.courses.interfaces import IPageRole

from eduintelligent.courses import coursesMessageFactory as _

# These are for everyone
    
class ManagerRole(object):
    implements(IPageRole)
    
    title = _(u"title_administrator", default=u"Instructor")
    required_permission = None

# class InstructorRole(object):
#     implements(IPageRole)
# 
#     title = _(u"title_instructor", default=u"Instructor")
#     required_permission = None

class StudentRole(object):
    implements(IPageRole)

    title = _(u"title_student", default=u"Student")
    required_permission = None

