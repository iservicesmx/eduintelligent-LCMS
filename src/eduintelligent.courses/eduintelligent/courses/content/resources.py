"""Definition of the Lessons content type.
"""

from zope.interface import implements

from Products.Archetypes import atapi

from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from eduintelligent.courses.interfaces import IResources
from eduintelligent.courses.config import PROJECTNAME
from eduintelligent.courses.utility import hideMetadataSchema
from eduintelligent.courses import coursesMessageFactory as _

CourseContentSchema = folder.ATFolderSchema.copy()

CourseContentSchema['title'].storage = atapi.AnnotationStorage()
CourseContentSchema['description'].storage = atapi.AnnotationStorage()

finalizeATCTSchema(CourseContentSchema, folderish=True, moveDiscussion=False)
hideMetadataSchema(CourseContentSchema, excludeFromNav=True)

class Resources(folder.ATFolder):
    """Contains multiple lessons.
    """
    implements(IResources)
    
    portal_type = "CourseContent"
    _at_rename_after_creation = True
    schema = CourseContentSchema
    
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

atapi.registerType(Resources, PROJECTNAME)
