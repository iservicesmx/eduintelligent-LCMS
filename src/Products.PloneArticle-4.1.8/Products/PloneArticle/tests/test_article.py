# -*- coding: utf-8 -*-
## Test case for PloneArticle content type
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
Test case for PloneArticle content type
"""

__docformat__ = 'restructuredtext'

#
from Acquisition import Implicit

# Products imports
from Products.PloneArticle.tests.common import BaseTestCase

class DummyAcquired(Implicit):
    """
    """
    portal_type = 'DummyAcquired'


class PloneArticleTestCase(BaseTestCase):
    """
    This class contains all test cases for PloneArticle content type.
    This content type is defined in : Products.PloneArticle.content.article
    """

    def afterSetUp(self):
        """ """
        self.loginAsPortalOwner()
        self.article = self.addPloneArticle(self.portal, 'article')
        self.logout()
    
    def testSkeleton(self):
        """Add new PloneArticle content and test its class skeleton"""        
        article = self.article
        
        # Test methods
        self.failUnless(hasattr(article, 'Title'))
        self.failUnless(hasattr(article, 'setTitle'))
        self.failUnless(hasattr(article, 'Description'))
        self.failUnless(hasattr(article, 'setDescription'))
        self.failUnless(hasattr(article, 'getText'))
        self.failUnless(hasattr(article, 'setText'))
        self.failUnless(hasattr(article, 'setImages'))
        self.failUnless(hasattr(article, 'getImages'))
        self.failUnless(hasattr(article, 'setFiles'))
        self.failUnless(hasattr(article, 'getFiles'))
        self.failUnless(hasattr(article, 'setLinks'))
        self.failUnless(hasattr(article, 'getLinks'))

    def testInterfaces(self):
        """
        Test presence of interfaces (+z3 interfaces obtained by ZCML)
        """
        from Products.PloneArticle.interfaces import INonStructuralFolder
        from Products.PloneArticle.interfaces import IPloneArticle
        from Products.ATContentTypes.interface import IATDocument

        article = self.article

        self.failUnless(INonStructuralFolder.isImplementedBy(article))
        self.failUnless(IPloneArticle.isImplementedBy(article))
        self.failUnless(IATDocument.isImplementedBy(article))

    def testVersionAtCreation(self):
        from Products.PloneArticle.version import CURRENT_ARTICLE_VERSION
        article = self.article

        self.assertEquals(article.getPAVersion(), CURRENT_ARTICLE_VERSION) 

    def testGetArticleObject(self):
        article = self.article

        dummy = DummyAcquired()
        acquired = dummy.__of__(article)
        result = acquired.getArticleObject()
        self.assertEqual(result, article)

    def testCopyArticle(self):
        self.loginAsPortalOwner()
        article = self.article
        
        # Add image
        image = self.addContent("Image", self.portal, "image1")
        
        # Reference this image to article
        data = [{
            'id': 'image1',
            'title': ('Inner image', {}), 
            'referencedContent': (image.UID(), {})}]
        article.setImages(data)
        
        # Copy article to new folder
        folder = self.addContent("Folder", self.portal, "folder")
        cb = self.portal.manage_copyObjects(ids=[article.getId()])
        folder.manage_pasteObjects(cb_copy_data=cb)
        article_copy = getattr(folder, article.getId())
        
        # Get references of proxy image
        refs = [(x.targetUID, x.relationship)
                for x in article.images.image1.getReferenceImpl()]
        refs_copy = [(x.targetUID, x.relationship)
                     for x in article_copy.images.image1.getReferenceImpl()]
        self.assertEqual(refs, refs_copy)

    def test_canSetDefaultPage(self):
        article = self.article
        self.loginAsPortalOwner()
        self.failIf(article.canSetDefaultPage())
        
    def test_Description(self):
        article = self.article
        text = """This is a dummy text"""
        self.loginAsPortalOwner()
        field = article.getField('description')
        mutator = field.getMutator(self.article)
        mutator(text)
        accessor = field.getEditAccessor(self.article)
        self.assertEquals(accessor(), text)
        
    def test_SearchableText(self):
        """Test if article SearchableText method returns the correct value 
        for SearchableText index"""
        
        article = self.article
        self.loginAsPortalOwner()
        article.setTitle('Article title')
        file_values = ({'id': 'object_1',
                        'title': 'Title 1',
                        'attachedFile': 'This is a dummy text'},
                       {'id': 'object_2',
                        'title': 'Title 2',
                        },)
        article.setFiles(file_values)
        expected_value = '1 2 a article article dummy is text this title title title'
        value = article.SearchableText()
        value_list = [x.lower() for x in value.split(" ") if x]
        value_list.sort()
        value = " ".join(value_list)
        self.assertEquals(value, expected_value)
    
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(PloneArticleTestCase))
    return suite
