# -*- coding: utf-8 -*-
## PloneArticle
## 
## Copyright (C) 2006 Ingeniweb

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
Test case for PloneArticle FTIs
"""

__docformat__ = 'restructuredtext'

from Products.Archetypes.atapi import registerType

# Products imports
from Products.PloneArticle.pafti import PloneArticleFactoryTypeInformation
from Products.PloneArticle.tests.common import BaseTestCase

class PAFTITestCase(BaseTestCase):
    """
    Tests for pafti.PloneArticleFactoryTypeInformation
    """
    def afterSetUp(self):

        # which one is best for our tests?
        #self.fti = PloneArticleFactoryTypeInformation('PloneArticle').__of__(self.portal)
        self.fti = self.portal.portal_types['PloneArticle']

    def test_PA_content_FTI(self):
        self.assert_(isinstance(self.fti, PloneArticleFactoryTypeInformation))
        
    def test_getAvailableReferenceableAttachmentTypes(self):
        self.assertEquals(self.fti.getAvailableReferenceableAttachmentTypes(),
                          ['File'])

    def test_getAvailableReferenceableImageTypes(self):
        value = self.fti.getAvailableReferenceableImageTypes()
        value.sort()
        expected_value = ['Image', 'News Item',]
        expected_value.sort()
        self.assertEquals(value, expected_value)

    def test_getAvailableReferenceableLinkTypes(self):
        value = self.fti.getAvailableReferenceableLinkTypes()
        value.sort()
        expected_value = ['Image', 'Topic', 'Large Plone Folder', 'Document',
            'PloneArticleMultiPage', 'Favorite', 'Event', 'Folder', 'Link', 
            'News Item', 'File', 'PloneArticle',]
        expected_value.sort()
        self.assertEquals(value, expected_value)

class DynamicAllowedContentFTITestCase(BaseTestCase):
    """
    Tests for pafti.DynamicAllowedContentFTI
    """

    def afterSetUp(self):
        self.fti = self.portal.portal_types['InnerContentContainer']

    def test_allowType(self):
        """Test that only IBaseInnerContent types are allowed"""
        fti = self.fti
        self.assertEquals(fti.allowType('FileInnerContentProxy'), True)
        self.assertEquals(fti.allowType('ImageInnerContentProxy'), True)
        self.assertEquals(fti.allowType('File'), False)
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(PAFTITestCase))
    suite.addTest(makeSuite(DynamicAllowedContentFTITestCase))
    return suite

