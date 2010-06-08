# -*- coding: utf-8 -*-
"""Definition of the CourseFolder content type.
"""

from zope.interface import implements
from zope.schema import fieldproperty
from zope.component import adapts, adapter, getMultiAdapter, getUtility

from zope.app.container.interfaces import INameChooser

from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping

from Acquisition import aq_inner, aq_parent
from Products.Archetypes.interfaces import IObjectInitializedEvent
from Products.CMFCore.utils import getToolByName

from BTrees.OOBTree import OOSet
from BTrees.OOBTree import OOBTree
from Products.Archetypes import atapi
from Products.validation import V_REQUIRED

from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from eduintelligent.courses.interfaces import ICourse, IBannerProvider
from eduintelligent.courses.config import PROJECTNAME, COURSEBOX_PORTLET_COLUMN
from eduintelligent.courses.utility import hideMetadataSchema
from eduintelligent.courses.portlets import coursebox

from eduintelligent.courses import coursesMessageFactory as _

CourseSchema = folder.ATBTreeFolderSchema.copy() + atapi.Schema((
   
    atapi.StringField('courseCode',
       #required=True,
       searchable=True,
       storage=atapi.AnnotationStorage(),
       widget=atapi.StringWidget(label=_(u"Course code"),
                                 description=_(u"This should match the course code used in the "
                                                "booking system."))
       ),
    # By using the name 'image' we can have the image show up in preview
    # folder listings for free
    atapi.ImageField('image',
        #required=True,
        languageIndependent=True,
        storage=atapi.AnnotationStorage(),
        swallowResizeExceptions=True,
        #pil_quality=90,
        #pil_resize_algo='antialias',
        max_size='no',
        sizes={'preview' : (400, 400),
              'mini'    : (200, 200),
              'icon'    :  (32, 32),
              },
        validators=(('isNonEmptyFile', V_REQUIRED),
                   ('checkImageMaxSize', V_REQUIRED)),
        widget=atapi.ImageWidget(label= _(u"Course image"),
                                description = _(u""),
                                show_content_type = False,),
       ),

    atapi.TextField('courseObjetives',
        #required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        validators=('isTidyHtmlWithCleanup',),
        default_output_type='text/x-html-safe',
        widget=atapi.RichWidget(label=_(u"Objetives"),
                               description=_(u"Write the course objetives, (is different to course's description)"),
                               rows=15,
                               allow_file_upload=False),
        ),

    atapi.StringField('courseCategory',
       required=True,
       searchable=True,
       vocabulary='getCategories',
       storage=atapi.AnnotationStorage(),
       widget=atapi.SelectionWidget(label=_(u"Category"),
                                 description=_(u"Select the category"))
       ),
    atapi.DateTimeField('startDate',
       #required=True,
       searchable=False,
       accessor='start',
       #default_method=DateTime, # Default to current date
       languageIndependent=True,
       storage=atapi.AnnotationStorage(),
       widget=atapi.CalendarWidget(label=_(u"Start Date"),
                                   description=_(u""),
                                   show_hm=False),
       ),

    atapi.DateTimeField('endDate',
       #required=True,
       searchable=False,
       accessor='end',
       #default_method=DateTime, # Default to current date
       languageIndependent=True,
       storage=atapi.AnnotationStorage(),
       widget=atapi.CalendarWidget(label=_(u"End Date"),
                                   description=_(u""),
                                   show_hm=False),
       ),
       atapi.LinesField('instructor',
          #required=True,
          searchable=True,
          storage=atapi.AnnotationStorage(),
          widget=atapi.LinesWidget(label=_(u"Course code"),visible=False)
          ),
      atapi.StringField('registered',
         #required=True,
         storage=atapi.AnnotationStorage(),
         widget=atapi.StringWidget(label=_(u"Course code"),visible=False)
         ),

      atapi.IntegerField("vigencyDays",
                required=False,
                default=365,
                storage=atapi.AnnotationStorage(),
                widget=atapi.IntegerWidget(
                     label=_(u'Course expiration period'),
                     description=_(u'Defines the number of days the course stays open.'),
                ),
         ),
         
       
       
))

CourseSchema['title'].storage = atapi.AnnotationStorage()
CourseSchema['description'].storage = atapi.AnnotationStorage()

finalizeATCTSchema(CourseSchema, folderish=True, moveDiscussion=False)
hideMetadataSchema(CourseSchema, excludeFromNav=True)

class Course(folder.ATBTreeFolder):
    """An ATBTreeFolder that contains course-related items.
    """
    implements(ICourse)
    
    portal_type = "Course"
    _at_rename_after_creation = True
    schema = CourseSchema
    
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    course_code = atapi.ATFieldProperty('courseCode')
    start_date = atapi.ATDateTimeFieldProperty('startDate')
    end_date = atapi.ATDateTimeFieldProperty('endDate')
    category = atapi.ATFieldProperty('courseCategory')
    objetives = atapi.ATFieldProperty('courseObjetives')
    vigency = atapi.ATFieldProperty('vigencyDays')

    # These two methods allow Plone to display the contained image
    # in its standard folder listings, and supports proper rendering
    # of scaled images. They are borrowed from ATContentTypes's ATNewsItem
    # class.
    
    def __init__(self, id=None):
        super(Course, self).__init__(id)
        self.attended_users = OOBTree() # userid -> DateTime

    def initStorageUsers(self):
        if not hasattr(self, 'attended_users'):
            setattr(self, 'attended_users', OOBTree())

    
    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        return self.getField('image').tag(self, **kwargs)

    def __bobo_traverse__(self, REQUEST, name):
        """Give transparent access to image scales. This hooks into the
        low-level traversal machinery, checking to see if we are trying to
        traverse to /path/to/object/image_<scalename>, and if so, returns
        the appropriate image content.
        """
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image

        return super(Course, self).__bobo_traverse__(REQUEST, name)


    
    def getCategories(self, prefix=''):
        parent = self.aq_inner.aq_parent
        return parent.getCategories()
        
    def getLocalRoles(self, role):
        #context = aq_inner(self.context)
        membership = getToolByName(self, 'portal_membership')
        portal = getToolByName(self, 'portal_url').getPortalObject()
        acl_users = getattr(portal, 'acl_users')

        result = []
        local_roles = self.get_local_roles()
        for name, roles in local_roles:
        #local_roles = acl_users.getLocalRolesForDisplay(self)    
        #for name, roles, rtype, rid in local_roles:
            for r in roles:
                if r == role:                    
                    member = acl_users.getUserById(name)
                    #member = acl_users.getUserById(rid)
                    if member is not None:
                        name = member.getProperty('fullname') or name
                        result.append(name)
        return result
        
    def getRegisteredStudents(self):
        #cuanto gasta de tiempo esto?? cada vez que es llamado desde la vista de curso
        #seria recomendable que mejor se guarde este campo en un archetype 
        #para que no gaste procesador cada vez que se 
        role='Student'
        pg = getToolByName(self, 'portal_groups')
        
        portal = getToolByName(self, 'portal_url').getPortalObject()
        acl_users = getattr(portal, 'acl_users')

        result = []
        local_roles = acl_users.getLocalRolesForDisplay(self)    
        for name, roles, rtype, rid in local_roles:
            if rtype == 'user':
                if role in roles:
                    result.append(rid)
            elif rtype == 'group':
                group = pg.getGroupById(rid)
                if group:
                    members = group.getGroupMembers()
                    for member in members:
                        mid = member.getId()
                        if not mid in result:
                            result.append(mid)
        return result
    
    def getPublishState(self):
        """
        """
        wftool = getToolByName(self, "portal_workflow")
        return wftool.getInfoFor(self, 'review_state')

            
atapi.registerType(Course, PROJECTNAME)

# This simple adapter uses Archetypes' ImageField to extract an HTML tag
# for the banner image. This is used in the promotions portlet to avoid
# having a hard dependency on the AT ImageField implementation.

# Note that we adapt a class, not an interface. This means that we will only
# match adapter lookups for this class (or a subclass), which is correct in
# this case, because we are relying on internal implementation details.

#TODO: Realmente usamos BannerProvider?? No lo creo!!

class BannerProvider(object):
    implements(IBannerProvider)
    adapts(Course)
    
    def __init__(self, context):
        self.context = context
    
    @property
    def tag(self):
        return self.context.getField('image').tag(self.context, scale='mini')


# We will register this function as an event handler, adding a "promotions"
# portlet whenever a cinema folder is first created. 
@adapter(ICourse, IObjectInitializedEvent)
def add_course_portlet(obj, event):
    
    # Only do this if the parent is not a course, i.e. only do it on
    # top-level course. Of course, site managers can move things 
    # around once the site structure is created
    
    parent = aq_parent(aq_inner(obj))
    if ICourse.providedBy(parent):
        return
    
    # A portlet manager is akin to a column
    column = getUtility(IPortletManager, name=COURSEBOX_PORTLET_COLUMN)
    
    # We multi-adapt the object and the column to an assignment mapping,
    # which acts like a dict where we can put portlet assignments
    manager = getMultiAdapter((obj, column,), IPortletAssignmentMapping)
    
    # We then create the assignment and put it in the assignment manager,
    # using the default name-chooser to pick a suitable name for us.
    assignment = coursebox.Assignment()
    chooser = INameChooser(manager)
    manager[chooser.chooseName(None, assignment)] = assignment
