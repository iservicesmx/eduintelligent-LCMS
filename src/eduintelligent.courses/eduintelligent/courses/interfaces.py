from zope.interface import Interface
from zope import schema

from zope.app.container.constraints import containers, contains
from plone.app.vocabularies.users import UsersSource
from plone.app.vocabularies.groups import GroupsSource

from eduintelligent.courses import coursesMessageFactory as _

class ICourseFolder(Interface):
    """A folder containing courses
    """
    contains('.ICourse')
    
    title = schema.TextLine(title=_(u"Title"),
                            required=True)
                            
    description = schema.TextLine(title=_(u"Description"),
                                  description=_(u"A short summary of this folder"))
                                  
    categories = schema.List(title=_(u"Categories"),
                     description=_(u"Classify this Course using the listed categories"),
                     required=True)

    
class ICourse(Interface):
    """A Course
    """  
    #containers('.ICourseFolder')  
    
    title = schema.TextLine(title=_(u"Course title"),
                            required=True)
    
    description = schema.TextLine(title=_(u"Description"),
                              description=_(u"Plain-text blurb about the course"))
    
    course_code = schema.ASCIILine(title=_(u"Course Code"),
                               description=_(u"This should match the course code used by the booking system"),
                               required=True)
    objetives = schema.SourceText(title=_(u"Objetives"),
                              description=_(u"A objetives of the course"),
                              required=True)
        
    start_date = schema.Date(title=_(u"Visible from"),
                             description=_(u"Date when course first appears on the website"))
    
    end_date = schema.Date(title=_(u"Visible until"),
                             description=_(u"Date when course last appears on the website"))
                             
    category = schema.TextLine(title=_(u"Category"), required=True)

# Adapters providing additional functionality for content types

class IBannerProvider(Interface):
    """A component which can provide an HTML tag for a banner image
    """

    tag = schema.TextLine(title=_(u"A HTML tag to render to show the banner image"))


class ILessons(Interface):
    """A folder containing sco, modules, lessons, etc.
    """
    #contains('eduintelligent.sco.interfaces.ISCO')

    title = schema.TextLine(title=_(u"Title"),
                            required=True)

    description = schema.TextLine(title=_(u"Description"),
                                  description=_(u"A short summary of this folder"))


class ICourseContent(Interface):
    """A folder containing sco, modules, lessons, etc.
    """
    title = schema.TextLine(title=_(u"Title"), required=True)
    description = schema.TextLine(title=_(u"Description"),
                                  description=_(u"A short summary of this folder"))

class IResources(Interface):
    """A folder containing resources.
    """
    title = schema.TextLine(title=_(u"Title"), required=True)
    description = schema.TextLine(title=_(u"Description"),
                                    description=_(u"A short summary of this folder"))


class IPageRole(Interface):
    """A named utility providing information about roles that are managed
    by the sharing page.

    Utility names should correspond to the role name.
    
    Es la interface para asignar los roles al curso. Los permisos son de
    estudiante e instructor.
    """

    title = schema.TextLine(title=u"A friendly name for the role")

    required_permission = schema.TextLine(title=u"Permission required to manage this local role",
                                          required=False)

