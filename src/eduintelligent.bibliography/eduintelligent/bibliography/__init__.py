# -*- coding: utf-8 -*-
#
# File: __init__.py
#
# Copyright (c) 2007 by ['Juan Ramon Lopez Beristain']
# Generator: ArchGenXML Version 2.0-alpha svn/development
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """iServices de Mexico <desarrollo@iservices.com.mx>"""
__docformat__ = 'plaintext'


# There are three ways to inject custom code here:
#
#   - To set global configuration variables, create a file AppConfig.py.
#       This will be imported in config.py, which in turn is imported in
#       each generated class and in this file.
#   - To perform custom initialisation after types have been registered,
#       use the protected code section at the bottom of initialize().

import logging
logger = logging.getLogger('eduintelligent.bibliography')
logger.debug('Installing Product')


from zope.i18nmessageid import MessageFactory
ebMessageFactory = MessageFactory('eduintelligent.bibliography')

import os
import os.path
from Globals import package_home
import Products.CMFPlone.interfaces
from Products.Archetypes import listTypes
from Products.Archetypes.atapi import *
from Products.Archetypes.utils import capitalize
from Products.CMFCore import DirectoryView
from Products.CMFCore import permissions as cmfpermissions
from Products.CMFCore import utils as cmfutils
from Products.CMFPlone.utils import ToolInit
from config import *

from zope.i18nmessageid import MessageFactory
ebMessageFactory = MessageFactory('eduintelligent.bibliography')

DirectoryView.registerDirectory('skins', product_globals)

##code-section custom-init-head #fill in your manual code here
##/code-section custom-init-head


def initialize(context):
    ##code-section custom-init-top #fill in your manual code here
    ##/code-section custom-init-top

    # imports packages and types for registration
    import content

    # Initialize portal content
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

    ##code-section custom-init-bottom #fill in your manual code here
    ##/code-section custom-init-bottom

