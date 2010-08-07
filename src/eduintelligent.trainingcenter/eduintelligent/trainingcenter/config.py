# config.py
import os.path
from Products.CMFCore.permissions import AddPortalContent
from Products.Archetypes.public import DisplayList
import Globals

PATH_IMPORT = os.path.join(Globals.INSTANCE_HOME, 'import')
PROJECTNAME	= "eduintelligent.trainingcenter"
DEFAULT_MEMBER_TYPE = 'eduMember'

SKINS_DIR	= "skins"
GLOBALS		= globals()

SUBGROUPS = DisplayList((
            ('company_position','Puesto'),
            ('company_division','Fuerza'),
            ('company_work_area','Región'),
            ))

GENDERS = DisplayList((
    ('m', 'Masculino'),
    ('f', 'Femenino'),
    ))


SCHOOLING = DisplayList((
        ('ninguno', 'Sin estudios'),
        ('primaria', 'Primaria'),
        ('secundaria', 'Secundaria'),
        ('preparatoria', 'Preparatoria/Bachiller'),
        ('universidad', 'Universidad'),        
        ('posgrado', 'Posgrado'),
        ('maestria', 'Maestría'),
        ('doctorado', 'Doctorado'),
        ('noespecificado', 'No especificado'),        
        )) 

COUNTRY_NAMES= (DisplayList((
    ("country_mexico","México"),
    ("country_argentina","Argentina"),
    ("country_bahamas","Bahamas"),
    ("country_barbados","Barbados"),
    ("country_belice","Belice"),
    ("country_bermudas","Bermudas"), 
    ("country_bolivia","Bolivia"),
    ("country_brasil","Brasil"),
    ("country_chile","Chile"),
    ("country_colombia","Colombia"),
    ("country_costa-rica","Costa Rica"),
    ("country_cuba","Cuba"),
    ("country_curacao","Curaçao"),
    ("country_republica-dominicana","República Dominicana"),
    ("country_ecuador","Ecuador"),
    ("country_el-salvador","El Salvador"),
    ("country_guatemala","Guatemala"),
    ("country_haiti","Haiti"),
    ("country_honduras","Honduras"),
    ("country_jamaica","Jamaica"),
    ("country_nicaragua","Nicaragua"),
    ("country_panama","Panamá"),
    ("country_paraguay","Paraguay"),
    ("country_peru","Perú"),
    ("country_puerto-rico","Puerto Rico"),
    ("country_estados-unidos","Estados Unidos"),
    ("country_tat","Trinidad and Tobago"),
    ("country_uruguay","Uruguay"),
    ("country_venezuela","Venezuela"),
    ))
)

#COUNTRY_NAMES = DisplayList(PAISES)

#ROLES_NAMES = DisplayList(ROLES)

