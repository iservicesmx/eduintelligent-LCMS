"""Definition of the CourseFolder content type.
"""

from zope.interface import implements

from Products.Archetypes import atapi

from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from eduintelligent.courses.interfaces import ICourseFolder
from eduintelligent.courses.config import PROJECTNAME
from eduintelligent.courses.utility import hideMetadataSchema
from eduintelligent.courses import coursesMessageFactory as _

CourseFolderSchema = folder.ATBTreeFolderSchema.copy() + atapi.Schema((
    atapi.LinesField('categories',
        storage=atapi.AnnotationStorage(),
        widget=atapi.LinesWidget(label=_(u"Categories"),
        description=_(u"One category on each line. Used for grouping courses. <br /> "
                      u"CAUTION: ONCE YOU ADD A NEW CATEGORY, YOU DON'T MODIFY OR DELETE THIS, ONLY YOU CAN ADD NEW CATEGORY"),
        rows=6,
        ),
    ),
))


CourseFolderSchema['title'].storage = atapi.AnnotationStorage()
CourseFolderSchema['description'].storage = atapi.AnnotationStorage()

finalizeATCTSchema(CourseFolderSchema, folderish=True, moveDiscussion=False)
hideMetadataSchema(CourseFolderSchema, excludeFromNav=True)

class CourseFolder(folder.ATBTreeFolder):
    """Contains multiple courses.
    """
    implements(ICourseFolder)
    
    portal_type = "Course Folder"
    _at_rename_after_creation = True
    schema = CourseFolderSchema
    
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    categories = atapi.ATFieldProperty('categories')

atapi.registerType(CourseFolder, PROJECTNAME)
