"""Definition of the Lessons content type.
"""

from zope.interface import implements

from Products.Archetypes import atapi

from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from eduintelligent.courses.interfaces import ILessons
from eduintelligent.courses.config import PROJECTNAME
from eduintelligent.courses.utility import hideMetadataSchema
from eduintelligent.courses import coursesMessageFactory as _

LessonsSchema = folder.ATBTreeFolderSchema.copy()


LessonsSchema['title'].storage = atapi.AnnotationStorage()
LessonsSchema['description'].storage = atapi.AnnotationStorage()

finalizeATCTSchema(LessonsSchema, folderish=True, moveDiscussion=False)
hideMetadataSchema(LessonsSchema, excludeFromNav=True)

class Lessons(folder.ATBTreeFolder):
    """Contains multiple lessons.
    """
    implements(ILessons)
    
    portal_type = "Lessons"
    _at_rename_after_creation = True
    schema = LessonsSchema
    
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

atapi.registerType(Lessons, PROJECTNAME)
