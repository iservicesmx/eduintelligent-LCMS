# -*- coding: utf-8 -*-
#
# File: Biblio.py
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

__author__ = """Juan Ramon Lopez Beristain <ramon@ro75.com>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *

try:
    from Products.LinguaPlone.public import *
except ImportError:
    HAS_LINGUAPLONE = False
else:
    HAS_LINGUAPLONE = True

from zope import interface
from zope.interface import implements
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema

from Products.eduBiblio.config import *
from Products.eduBiblio.interfaces import IBiblio


##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    LinesField(
        name='category',
        widget=LinesField._properties['widget'](
            label='Category',
            label_msgid='eduBiblio_label_category',
            i18n_domain='eduBiblio',
        )
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Biblio_schema = ATFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Biblio(ATFolder):
    """
    """
    security = ClassSecurityInfo()
    implements(IBiblio)
    meta_type = 'Biblio'
    _at_rename_after_creation = True

    schema = Biblio_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

registerType(Biblio, PROJECTNAME)
# end of class Biblio

##code-section module-footer #fill in your manual code here
##/code-section module-footer



