from zope.i18nmessageid import MessageFactory

from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore.utils import ContentInit
from Products.CMFCore.DirectoryView import registerDirectory

from config import *
from permissions import ADD_CONTENT_PERMISSIONS, DEFAULT_ADD_CONTENT_PERMISSION

TCMessageFactory = MessageFactory('eduinteligent.trainingcenter')

import logging
logger = logging.getLogger('eduinteligent.trainingcenter')
logger.info('Initialize Product')

registerDirectory(SKINS_DIR, GLOBALS)

def initialize(context):
    # Register Archetypes content types
    import content

    contentTypes, constructors, ftis = process_types(listTypes(PROJECTNAME), PROJECTNAME)

    ContentInit(
        PROJECTNAME + ' Content',
        content_types      = contentTypes,
        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

    for i in range(0, len(contentTypes)):
        klassname = contentTypes[i].__name__
        if not klassname in ADD_CONTENT_PERMISSIONS:
            continue
        context.registerClass(meta_type    = ftis[i]['meta_type'],
                              constructors = (constructors[i],),
                              permission   = ADD_CONTENT_PERMISSIONS[klassname])