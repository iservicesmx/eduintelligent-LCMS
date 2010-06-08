# -*- coding: utf-8 -*-
## Initialize PloneArticle product
## Copyright (C)2005 Ingeniweb

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING. If not, write to the
## Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
Initialize PloneArticle product
"""
__docformat__ = 'restructuredtext'

import os.path
import logging
LOG = logging.getLogger('PloneArticle')

__version__ = open(os.path.join(__path__[0], 'version.txt')).read().strip()
__version__ = __version__.lower()

# CMF imports
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore import DirectoryView
from Products.CMFCore.utils import ContentInit, ToolInit

# Archetypes imports
from Products.Archetypes.public import process_types, listTypes

# Products imports
from Products.PloneArticle import config
from Products.PloneArticle.pafti import PloneArticleFactoryTypeInformation
from Products.PloneArticle.pafti import manage_addPAFTIForm
from Products.PloneArticle.pafti import DynamicAllowedContentFTI
from Products.PloneArticle.pafti import manage_addDVTFTIForm

from Products.PloneArticle import content, proxy
from Products.PloneArticle import tool

from Products.PloneArticle import migration

# Register skin directories so they can be added to portal_skins
DirectoryView.registerDirectory('skins', config.GLOBALS)


def initialize(context):
    # Setup migrations
    migration.executeMigrations()
    migration.registerMigrations()

    # optional demo content
    if config.INSTALL_EXAMPLES:
        import examples

    # register the fti
    context.registerClass(
        PloneArticleFactoryTypeInformation,
        permission=ManagePortal,
        constructors=(manage_addPAFTIForm,),
        visibility=None)

    context.registerClass(
        DynamicAllowedContentFTI,
        permission=ManagePortal,
        constructors=(manage_addDVTFTIForm,),
        visibility=None)

    # initialize the content, including types and add permissions
    content_types, constructors, ftis = process_types(
        listTypes(config.PROJECTNAME),
        config.PROJECTNAME)

    permissions = {
        'PloneArticle': 'PloneArticle: Add PloneArticle',
        'PloneArticleMultiPage': "PloneArticle: Add PloneArticleMultiPage",
        }

    for atype, constructor, fti in zip(content_types, constructors, ftis):
        permission = permissions.get(atype.portal_type,
                                     'PloneArticle: Add PloneArticle')
        ContentInit(
            config.PROJECTNAME + ' Content',
            content_types=(atype,),
            permission= permission,
            extra_constructors=(constructor,),
            fti=(fti,),
        ).initialize(context)

    # Initialize the tool
    ToolInit(
        config.PROJECTNAME + ' Tool',
        tools=(tool.PloneArticleTool,),
        icon='tool.gif').initialize(context)
