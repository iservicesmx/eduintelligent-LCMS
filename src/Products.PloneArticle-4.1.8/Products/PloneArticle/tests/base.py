# -*- coding: utf-8 -*-
## Defines BaseTestCase class. Inherits from this class to make test cases
## on PloneArticle product
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
Defines BaseTestCase class. Inherits from this class to make test cases on
PloneArticle product
"""

__docformat__ = 'restructuredtext'

# Zope imports
from Testing import ZopeTestCase

# CMF imports
from Products.CMFCore.utils import getToolByName

# Plone imports
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.setup import PLONE21, PLONE25

class BaseTestCase(PloneTestCase.PloneTestCase):
    """Base class for all class with test cases on PloneArticle"""

    def _setup(self):
        PloneTestCase.PloneTestCase._setup(self)

    def addContent(self, portal_type, container, content_id, **kwargs):
        """Add new content"""

        container.invokeFactory(portal_type, id=content_id, **kwargs)
        content = getattr(container, content_id)
        return content

    def addPloneArticle(self, container, content_id, **kwargs):
        """Add PloneArticle content"""

        return self.addContent('PloneArticle', container, content_id)

ZopeTestCase.installProduct('PlacelessTranslationService')

# additional content type
from Products.Archetypes.atapi import Schema, BaseContentMixin, registerType
from Products.PloneArticle.config import PROJECTNAME
from Products.PloneArticle.field import SmartListField

ALLOWED_CRITERIAS = ('SearchableText', 'portal_type',)
schema = Schema((
    SmartListField('smartlistfield',
                   relationship='unit_test',
                   auto_reference=True,
                   ),
    SmartListField('restricted_smartlistfield',
                   relationship='unit_test_restricted',
                   allowed_types=('PloneArticle',),
                   allowed_criterias=ALLOWED_CRITERIAS,
                   )
    ))

class SimpleSmartContent(BaseContentMixin):
    """Content with a smartlist field
    """
    schema = schema

registerType(SimpleSmartContent, PROJECTNAME)


# Install Attachment field if it exists
from Products.PloneArticle.tool import USE_ATTACHMENT_FIELD

if USE_ATTACHMENT_FIELD:
    ZopeTestCase.installProduct('AttachmentField')

# Install PloneArticle
ZopeTestCase.installProduct('PloneArticle')

# Setup Plone site
if USE_ATTACHMENT_FIELD:
    PloneTestCase.setupPloneSite(products=['kupu', 'AttachmentField', 'PloneArticle'])
else:
    PloneTestCase.setupPloneSite(products=['kupu', 'PloneArticle'])
