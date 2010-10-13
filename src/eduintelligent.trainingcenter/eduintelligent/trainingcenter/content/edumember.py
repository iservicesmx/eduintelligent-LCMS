from AccessControl import ClassSecurityInfo, AuthEncoding
from Acquisition import aq_chain, aq_inner

from zope.interface import implements
from zope.component import getUtility, queryUtility, getMultiAdapter

from Products.CMFCore.utils import getToolByName

from Products.Archetypes.public import *

from Products.membrane.interfaces import IGroupsProvider
from Products.membrane.interfaces import IGroupAwareRolesProvider
from Products.remember.content.member import Member
from Products.remember.content.member_schema import id_schema, \
     contact_schema, plone_schema, security_schema, login_info_schema
#product

from eduintelligent.trainingcenter.config import *
from eduintelligent.trainingcenter.content.member_schema import member_schema
from eduintelligent.trainingcenter.interfaces import IEduMember
from eduintelligent.trainingcenter.permissions import AddMember

from eduintelligent.trainingcenter import TCMessageFactory as _

from DateTime import DateTime

SimpleSchema = Schema((
    StringField('FirstName',
                required=1,
                widget=StringWidget(
                    label=_(u'Name'), 
                    description=_('')
                    ),
                regfield=1,
                user_property=True,
                ),
    StringField('LastName',
                required=1,
                widget=StringWidget(
                    label=_(u'Last Name'),
                    description=_(u'')
                    ),
                regfield=1,
                user_property=True,
                ),
    contact_schema['email'],
    id_schema['id'],
    id_schema['title'],
    security_schema['password'],
    security_schema['confirm_password'],
    ComputedField('fullname',
                  expression='context.getFullname()',
                  searchable=1,
                  widget=ComputedWidget(
                      label=_(u'Full name'),
                      description=_(u''),
                      visible={'edit': 'invisible', 'view': 'invisible'},
                      ),
                  user_property=True,
                  ),
    #plone_schema['portrait'],
    #security_schema['roles'],
    #security_schema['groups'],
))

#member_schema = getattr(BaseMember, 'schema', Schema(())).copy() + SimpleSchema.copy()
security_schema = security_schema.copy()
del security_schema['password'],
del security_schema['confirm_password'],
#del security_schema['mail_me'],

for field in security_schema.fields():
    #field.schemata = 'Security'
    field.widget.visible = False

plone_schema = plone_schema.copy()
#del plone_schema['portrait'],
for field in plone_schema.fields():
    #field.schemata = 'Plone Settings'
    field.widget.visible = False

metadata_schema = ExtensibleMetadata.schema.copy()
for field in metadata_schema.fields():
    field.schemata = 'default'
    field.widget.visible = False

SimpleSchema = SimpleSchema.copy() + member_schema.copy() + security_schema + login_info_schema + metadata_schema + plone_schema

#property sheets can't handle images
Portrait = SimpleSchema['portrait']
Portrait.user_property = False
Portrait.widget.visible = True
Portrait.schemata = 'Personal'

IdField = SimpleSchema['id']
IdField.write_permission = AddMember


TitleField = SimpleSchema['title']
TitleField.required = 0
TitleField.widget.visible = False


class eduMember(Member):
    """A simple member archetype"""
    schema = SimpleSchema
    _at_rename_after_creation = True

    security = ClassSecurityInfo()
    portal_type = "eduMember"

    implements(IEduMember,
               IGroupAwareRolesProvider,
               # Mark users are given groups by containment or backrefs
               IGroupsProvider,
               )

    def getFullname(self):
        """ return Person's Fullname """
        fn = self.getFirstName()
        sn = self.getLastName()
        if fn or sn:
            return '%s %s' % (self.getFirstName(), self.getLastName())
        else:
            return ''

    Title = getFullname

    def showPasswordField(self):
        """Para que muestre los campos de Password"""
        return True

    ####### Validators ######
    def getValidGroups(self, prefix=''):
        parent = self.aq_inner.aq_parent
        parent = parent.getGroupId()
        tctool = getToolByName(self, 'portal_tctool')

        grps = tctool.getGroups(parent=parent, prefix=prefix)
        lst = []
        for grp in grps:
            lst.append((grp['id'],grp['title']))
        #print "grupo de",parent,prefix,":  \n",lst
        return lst


    def valid_division(self):
        return self.getValidGroups('company_division')

    def valid_work_area(self):
        return self.getValidGroups('company_work_area')

    def valid_position(self):
        return self.getValidGroups('company_position')
    
    ###################
    def getGroupName(self, groupid):
        """
        """
        portal_groups = getToolByName(self, 'portal_groups')
        group = portal_groups.getGroupById(groupid)
        name = group.getGroupTitleOrName()
        return name

    def getDivisionName(self):
        """
        """
        grps = []
        for grp in self.getCompany_division():
            grp = self.getGroupName(grp)
            grps.append(grp)
        return grps
    def getPositionName(self):
        grp = self.getCompany_position()
        if not grp:
            return ''
        return self.getGroupName(grp)

    def getSexName(self):
        """
        get the label by key
        """
        return GENDERS.getValue(self.getPersonal_gender())

    def getCivilianName(self):
        """
        get the label by key
        """
        return CIVILIAN.getValue(self.getPersonal_civilian())

    def getChildrenName(self):
        """
        get the label by key
        """
        return CHILDREN.getValue(self.getPersonal_children())

    def getSchoolingName(self):
        """
        get the label by key
        """
        return SCHOOLING.getValue(self.getPersonal_last_schooling())

    def getCountryName(self):
        """
        get the label by key
        """
        return COUNTRY_NAMES.getValue(self.getCountry())


    def getAge(self):
        """age"""
        birth = self.getPersonal_birthdate()
        if birth is None:
            return ""

        now = DateTime()
        year = now.year() - birth.year()
        if now.month() < birth.month() or (now.month() == birth.month() and now.day() < birth.day()):
            year = year -1

        return str(year)+" años"

    def getAntiquity(self):
        """antiquity"""
        antiquit = self.getCompany_employee_startdate()
        if antiquit is None:
            return ""

        now = DateTime()
        year = now.year() - antiquit.year()
        if now.month() < antiquit.month() or (now.month() == antiquit.month() and now.day() < antiquit.day()):
            year = year -1

        return str(year)+" años"

    # def setDynamicKardex(self, **kw):
    #     entry = {
    #         'course': '', 
    #         'date': '', 
    #         'evaluation': '', 
    #         'note': '', 
    #         'old': '', 
    #         'score': '', 
    #         'score2': '', 
    #         'type': '', 
    #     }
    #     kardex = list(self.getKardex())
    #     # print kardex
    #     # print "--------------"
    #     # print kw
    #     entry.update(kw)
    #     kardex.append(entry)
    #     # print "--------------"
    #     # print entry
    #     # print kardex
    #     self.setKardex(kardex)
    # 
    # def getTypeScore(self):
    #     """
    #     """
    #     return DisplayList(
    #         (("exam", _("Exam"),),
    #          ("activity", _("Activity"),),
    #          ("sco", _("SCORM"),),)
    #     )
    

registerType(eduMember, PROJECTNAME)
