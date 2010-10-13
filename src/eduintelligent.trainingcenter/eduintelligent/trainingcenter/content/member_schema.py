from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import *
from eduintelligent.trainingcenter.config import *
from eduintelligent.trainingcenter.permissions import ModifyMember

# from Products.DataGridField import DataGridField, DataGridWidget
# from Products.DataGridField.Column import Column
# from Products.DataGridField.FixedColumn import FixedColumn
# from Products.DataGridField.SelectColumn import SelectColumn
# from Products.DataGridField.LinkColumn import LinkColumn

from eduintelligent.trainingcenter import TCMessageFactory as _

from Products.remember.permissions import VIEW_PUBLIC_PERMISSION, \
     EDIT_ID_PERMISSION, VIEW_OTHER_PERMISSION, EDIT_PROPERTIES_PERMISSION, \
     VIEW_SECURITY_PERMISSION, EDIT_PASSWORD_PERMISSION, \
     EDIT_SECURITY_PERMISSION, MAIL_PASSWORD_PERMISSION, ADD_PERMISSION, \
     VIEW_PERMISSION, REGISTER_PERMISSION


# class LinkViewColumn(LinkColumn):
#     security = ClassSecurityInfo()
#     
#     def __init__(self, title):
#         """ Create a Link
#         """
#         LinkColumn.__init__(self, title)
# 
#     security.declarePublic('getMacro')
#     def getMacro(self):
#         """ Return macro used to render this column in view/edit """
#         return "datagrid_linkview_cell"    
    

member_schema = Schema((
    #______________________
    #Schemata: Default
    #First Name
    #Last Name
    #e-mail
    #login/username
    #password
    #Confirm Password
    StringField('country',
        vocabulary=COUNTRY_NAMES,
        read_permission=VIEW_PUBLIC_PERMISSION,
        write_permission=EDIT_ID_PERMISSION,
        widget=SelectionWidget(
            label = _(u'Country'),
            description = _(u'Choose your country'),
        ),
    ),
    StringField('phone',
        searchable=1,        
        widget=StringWidget(
            label = _(u'Phone'),
            description = _(u'Contact Phone number'),
        ),
    ),
    
    #______________________
    #Schemata: Company
    StringField('company_employee_number',
        schemata=_(u'Work'),
        searchable=1,
        read_permission=VIEW_PUBLIC_PERMISSION,
        write_permission=EDIT_ID_PERMISSION,        
        widget=StringWidget(
            label = _(u'Employee Number'),
            description = _(u"Employee's ID"),
        ),
    ),
    StringField('company_work_area',
        schemata=_(u'Work'),
        #searchable=1,
        read_permission=VIEW_PUBLIC_PERMISSION,
        write_permission=EDIT_ID_PERMISSION,        
        vocabulary='valid_work_area',
        enforceVocabulary=1,
        mode='rw',
        read_permissions=ModifyMember,
        write_permissions=ModifyMember,
        widget=SelectionWidget(
            label = _(u'Work Area'),
            description = _(u"Employee's designated work area"),
        ),
    ),
    StringField('company_position',
        schemata=_(u'Work'),
        #searchable=1,
        vocabulary='valid_position',
        read_permission=VIEW_PUBLIC_PERMISSION,
        write_permission=EDIT_ID_PERMISSION,
        enforceVocabulary=1,
        widget=SelectionWidget(
            label = _(u'Position'),
            description = _(u"Employee's position on this company"),
        ),
    ), 
    LinesField ('company_division',
        schemata=_(u'Work'),
        read_permission=VIEW_PUBLIC_PERMISSION,
        write_permission=EDIT_ID_PERMISSION,
        vocabulary='valid_division',
        enforceVocabulary=1,
        multiValued=1,
        widget=MultiSelectionWidget(
            label = _(u'Division'),
            description = _(u"Company Division to which the employee belongs to"),
            visible=1,
        ),
    ),    
    DateTimeField('company_employee_startdate',
        schemata=_(u'Work'),
        widget=CalendarWidget(
            label = _(u"Employee's Start date"),
            description = _(u"The employee's starting date on this company"),
            show_hm=False,
            starting_year=1900,
            visible=0,
        ),
    ),
    ComputedField('company_employee_seniority',
        expression='context.getAntiquity()',
        schemata=_(u'Work'),
        widget=StringWidget(
            label = _(u'Seniority'),
            description = _(u"The employee's seniority")
        ),
    ),    
    StringField('company_company',
        schemata=_(u'Work'),
        widget=StringWidget(
            label = _(u'Company'),
            description = _(u''),
            visible=0,
        ),
    ),

    #______________________
    #Schemata: Location
    StringField('state',
        schemata=_(u'Location'),
        searchable=1,
        widget=StringWidget(
            label = _(u'State'),
            description = _(u'Country State where you work or live'),
        ),
    ),
    StringField('location_plaza',
        schemata=_(u'Location'),
        searchable=1,
        read_permission=VIEW_PUBLIC_PERMISSION,
        write_permission=EDIT_ID_PERMISSION,        
        widget=StringWidget(
            label = _(u'Plaza'),
            description = _(u'')
        ),
        ),     
    StringField('location_region',
        schemata=_(u'Location'),
        searchable=1,
        read_permission=VIEW_PUBLIC_PERMISSION,
        write_permission=EDIT_ID_PERMISSION,        
        widget=StringWidget(
            label = _(u'Region'),
            description = _(u'')
        ),
        ),     
    

    #______________________
    #Schemata: Personal
    DateTimeField('personal_birthdate',
        schemata=_(u'Personal'),
        widget=CalendarWidget(
            label = _(u'Birth Date'),
            description = _(u''),
            show_hm=False,
            starting_year=1900,
        ),
    ),
    ComputedField('personal_age',
        expression='context.getAge()',
        schemata=_(u'Personal'),
        widget=StringWidget(
            label = _(u'Age'),
            description = _(u''),
        ),
    ),
    StringField('personal_schooling',
        schemata=_(u'Personal'),
        vocabulary=SCHOOLING,
        widget=SelectionWidget(
            label = _(u'Schooling'),
            description = _(u''),
        ),
    ),    
    StringField('personal_residence',
        schemata=_(u'Personal'),
        searchable=1,
        widget=StringWidget(
            label = _(u'Residence Address'),
            description = _(u'Home Address (optional)')
        ),
    ),
    StringField('personal_phone',
        schemata=_(u'Personal'),
        searchable=1,
        widget=StringWidget(
            label = _(u'Personal phone number'),
            description = _(u'Personal or Home phone number (Optional)')
        ),
    ),    
    StringField('personal_gender',
        schemata=_(u'Personal'),
        vocabulary=GENDERS,
        widget=SelectionWidget(
            label = _('Gender'),
            description = _(u'')
        ),
    ),    
    StringField('personal_last_school',
        schemata=_(u'Personal'),
        widget=StringWidget(
            label = _(u'Last School Degree'),
            description = _(u'Describe the last degree, diploma or trainning you took.')
        ),
    ),
    #______________________
    #Hidden / Others
    StringField('group',
        schemata=_(u'Personal'),
        widget=StringWidget(
            label = _(u'Personal'),
            description = _(u''),
            visible=0
        ),
    ),
    StringField('main_group',
        accessor='getMain_group', 
        mutator='setMain_group',
        widget=StringWidget(
            label = _(u"Main Group"),
            visible = {'edit':'invisible','view':'visible'},
    ),
    user_property=True,
    ),
    
    ## Se elimina por falta de documentación
    # DataGridField('kardex',
    #         schemata = 'Kardex',
    #         read_permission=VIEW_PUBLIC_PERMISSION,
    #         write_permission=EDIT_ID_PERMISSION,
    #         columns=('old', 'course', 'evaluation', 'type', 'date', 'score', 'score2', 'note'),
    #         widget = DataGridWidget(
    #             columns= {
    #                 'old' : FixedColumn("Old", visible=False),
    #                 'course' : FixedColumn(_("Course")),
    #                 'evaluation' : LinkViewColumn(_("Evaluation")),
    #                 'type' : SelectColumn(_("Type"), vocabulary="getTypeScore"),
    #                 'date' : FixedColumn(_("Date")),
    #                 'score' : FixedColumn(_("Score")),
    #                 'score2' : Column(_("Extra")),
    #                 'note' : Column(_("Note")),
    #             },
    #         ),
    #         auto_insert = False,
    #         allow_insert=False,
    #         allow_delete=True,
    #         allow_reorder=False,        
    # ),
   
),)
