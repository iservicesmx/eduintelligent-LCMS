from AccessControl import ClassSecurityInfo, AuthEncoding

from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.public import BaseSchema, Schema
from Products.ATContentTypes.content.folder import ATBTreeFolder 
from Products.ATContentTypes.lib import constraintypes
from Products.Archetypes.public import registerType
from Products.Archetypes.public import LinesField, MultiSelectionWidget, KeywordWidget
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFCore.utils import getToolByName

from Products.membrane.interfaces import IGroup
from Products.membrane.interfaces import IMembraneUserAuth
from Products.membrane.config import TOOLNAME as MEMBRANE_TOOL
from Products.membrane.utils import getFilteredValidRolesForPortal

from Products.UserField.field import UserField

from eduintelligent.trainingcenter.config import PROJECTNAME
from eduintelligent.trainingcenter.interfaces import ITrainingCenter

from eduintelligent.trainingcenter import TCMessageFactory as _

schema = Schema((
    UserField(name='administators', 
            schemata='Administradores', 
            localrole='Manager',
            #cumulative=True, 
            multiValued=True),
    UserField(name='instuctors', 
            schemata='Instructores', 
            localrole='Administrator', 
            #cumulative=True, 
            multiValued=True),
    LinesField(
        # not 'roles' b/c 'validate_roles' exists; stoopid Archetypes
        name="roles_",
        accessor='getRoles',
        languageIndependent=1,
        vocabulary='getRoleSet',
        multiValued=1,
        widget=MultiSelectionWidget(
            label=_(u"Roles"),
            description=_(u"Roles that members of this group should receive."),
            visible = False
            ),
        ),

),)

SimpleSchema = getattr(ATBTreeFolder, 'schema', Schema(())).copy() + schema.copy()

# Ugly hack to hide metadata fields
for field in SimpleSchema.fields():
    if field.isMetadata:
        field.schemata = 'default'
        field.widget.visible = False
        
DescField = SimpleSchema['description']
DescField.widget.visible = True

AdminField = SimpleSchema['administators']
AdminField.widget.label=_(u'Administrators')

InstField = SimpleSchema['instuctors']
InstField.widget.label=_(u'Instructors')

    
class TrainingCenter(BrowserDefaultMixin, ATBTreeFolder):
    """A simple group archetype"""
    schema = SimpleSchema
    portal_type = "TrainingCenter"
    _at_rename_after_creation = True
    #__implements__ = (getattr(ATBTreeFolder,'__implements__',()),
    #                    getattr(BrowserDefaultMixin,'__implements__',()))
    __implements__ = (ATBTreeFolder.__implements__ +
                          BrowserDefaultMixin.__implements__)
    implements(ITrainingCenter, IGroup)

    security = ClassSecurityInfo()
    #displayContentsTab = False

    def initializeArchetype(self, **kwargs):
        """
        """
        wftool = getToolByName(self, "portal_workflow")
        ATBTreeFolder.initializeArchetype(self,**kwargs)


        if 'news' not in self.objectIds():
            _createObjectByType('Large Plone Folder',self, 'news')
            obj = self['news']
            obj.setTitle(self.translate(
                    msgid='news_title',
                    domain='eduintelligent.trainingcenter',
                    default='News'))
            obj.setDescription(self.translate(
                    msgid='news_description',
                    domain='eduintelligent.trainingcenter',
                    default='Site News')) 
            obj.setConstrainTypesMode(constraintypes.ENABLED)
            obj.setLocallyAllowedTypes(['News Item'])
            obj.setImmediatelyAddableTypes(['News Item']) 
            obj.setLayout('folder_summary_view')
            obj.unmarkCreationFlag() #??????
            
            if wftool.getInfoFor(obj, 'review_state') != 'published':
                wftool.doActionFor(obj, 'publish')
            obj.reindexObject()

        if 'events' not in self.objectIds():
            _createObjectByType('Large Plone Folder',self, 'events')
            obj = self['events']
            obj.setTitle(self.translate(
                    msgid='events_title',
                    domain='eduintelligent.trainingcenter',
                    default='Events'))
            obj.setDescription(self.translate(
                    msgid='events_description',
                    domain='eduintelligent.trainingcenter',
                    default='Site Events'))
            obj.setConstrainTypesMode(constraintypes.ENABLED)
            obj.setLocallyAllowedTypes(['Event'])
            obj.setImmediatelyAddableTypes(['Event'])
            obj.setLayout('folder_summary_view')
            obj.unmarkCreationFlag() #??????

            if wftool.getInfoFor(obj, 'review_state') != 'published':
                wftool.doActionFor(obj, 'publish')
            obj.reindexObject()


        if 'polls' not in self.objectIds():
            _createObjectByType('Large Plone Folder',self, 'polls')
            obj = self['polls']
            obj.setTitle(self.translate(
                    msgid='poll_title',
                    domain='eduintelligent.trainingcenter',
                    default='Polls'))
            obj.setDescription(self.translate(
                    msgid='poll_description',
                    domain='eduintelligent.trainingcenter',
                    default='Site Polls'))
            obj.setConstrainTypesMode(constraintypes.ENABLED)        
            obj.setLocallyAllowedTypes(['PlonePopoll'])
            obj.setImmediatelyAddableTypes(['PlonePopoll'])
            obj.setLayout('folder_summary_view')
            obj.unmarkCreationFlag()
        
            if wftool.getInfoFor(obj, 'review_state') != 'published':
                wftool.doActionFor(obj, 'publish')
            obj.reindexObject()


        if 'courses' not in self.objectIds():
            _createObjectByType('Course Folder',self, 'courses')
            obj = self['courses']
            obj.setTitle(self.translate(
                    msgid='courses_title',
                    domain='eduintelligent.trainingcenter',
                    default='Courses'))
            obj.setDescription(self.translate(
                    msgid='courses_description',
                    domain='eduintelligent.trainingcenter',
                    default='Courses Folder'))
        
            #if wftool.getInfoFor(obj, 'review_state') != 'active':
                #wftool.doActionFor(obj, 'activate')
            obj.reindexObject()
    
    def getGroupName(self):
        return self.getId()

    #####################################################
    # IGroup implementation
    # NOTE: Title() and getRoles() are autogenerated
    #####################################################
    def getGroupId(self):
        return self.getId()
        
    def getGroupMembers(self):
        # All references and all subobjects that are members
        mt = getToolByName(self, MEMBRANE_TOOL)
        usr = mt.unrestrictedSearchResults
        members = {}
        for m in usr(object_implements=IMembraneUserAuth.__identifier__,
                     path='/'.join(self.getPhysicalPath())):
            members[m.getUserId] = 1
        print members.keys()
        return tuple(members.keys())
 
    # def listUsers(self):
    #     """
    #     Return a DisplayList of users
    #     """
    #     catalog = getToolByName(self, TOOLNAME)
    # 
    #     results = catalog(object_implements=IMembraneUserAuth.__identifier__)
    #     value = []
    #     for r in results:
    #         key = r.getUserName is not None and \
    #               r.getUserName.strip() or r.getUserId
    #         value.append((key.lower(), (r.UID, key)))
    #     value.sort()
    #     value = [r for throwaway, r in value]
    #     value.insert(0, ('', '<no reference>'))
    #     return DisplayList(value)

    getRoleSet = getFilteredValidRolesForPortal

registerType(TrainingCenter, PROJECTNAME)
