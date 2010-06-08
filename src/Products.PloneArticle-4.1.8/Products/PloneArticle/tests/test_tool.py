# -*- coding: utf-8 -*-
## Test case for PloneArticleTool
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
Test case for all InnerContentProxy classes
"""

__docformat__ = 'restructuredtext'

# CMF imports
from Products.CMFCore.utils import getToolByName

# Products imports
from Products.PloneArticle.config import PLONEARTICLE_TOOL
from Products.PloneArticle.tests.common import BaseTestCase

expected_ref_types = {
    'PloneArticle': {
        'files': ['File'],
        'images': ['Image', 'News Item'],
        'links': ['Image', 'Topic', 'Large Plone Folder', 'Document', \
            'PloneArticleMultiPage', 'Favorite', 'Event', 'Folder', 'Link', \
            'News Item', 'File', 'PloneArticle']
        }
    }

update_types = {
    'PloneArticle': {
        'images': ['Image', 'Link'],
        'links': ['Link',]
        }
    }

updated_ref_types = {
    'PloneArticle': {
        'files': ['File'],
        'images': ['Image',],
        'links': ['Link',]
        }
    }

class FakeImage:
    def __init__(self):
        self.width = 200
        self.height = 160

class ArticleToolTestCase(BaseTestCase):
    """
    Test PloneArticleTool
    """

    def afterSetUp(self):
        self.tool = getToolByName(self.portal, PLONEARTICLE_TOOL)

    def testUpdateReferenceableTypes(self):
        tool = self.tool
        self.failUnless(hasattr(tool, 'referenceable_types'))
        
        tool.updateReferenceableTypes()               
        ref_types = tool.referenceable_types
        for schema_id in ('files', 'images', 'links'):
            value = ref_types['PloneArticle'][schema_id]
            value.sort()
            expected_value = expected_ref_types['PloneArticle'][schema_id]
            expected_value.sort()
            self.assertEqual(value, expected_value)

        tool.updateReferenceableTypes(updates=update_types)
        ref_types = tool.referenceable_types
        self.assertEqual(ref_types, updated_ref_types)
        self.failIf('Link' in ref_types['PloneArticle']['images'])

        del tool.referenceable_types['PloneArticle']['files']
        tool.updateReferenceableTypes()   
        ref_types = tool.referenceable_types
        value = ref_types['PloneArticle']['files']
        value.sort()
        expected_value = expected_ref_types['PloneArticle']['files']
        expected_value.sort()
        self.assertEqual(value, expected_value)

        tool.updateReferenceableTypes(reset=True)
        ref_types = tool.referenceable_types
        for schema_id in ('files', 'images', 'links'):
            value = ref_types['PloneArticle'][schema_id]
            value.sort()
            expected_value = expected_ref_types['PloneArticle'][schema_id]
            expected_value.sort()
            self.assertEqual(value, expected_value)

        tool.updateReferenceableTypes(updates=update_types, reset=True)
        ref_types = tool.referenceable_types
        for schema_id in ('files', 'images', 'links'):
            value = ref_types['PloneArticle'][schema_id]
            value.sort()
            expected_value = expected_ref_types['PloneArticle'][schema_id]
            expected_value.sort()
            self.assertEqual(value, expected_value)
        
    def testGetScaleSize(self):
        tool = self.tool
        img = FakeImage()
        expected_sizes = (100, 80)
        self.assertEqual(tool._getScaleSize(img, 100, 80), expected_sizes)
        expected_sizes = (100, 80)
        self.assertEqual(tool._getScaleSize(img, 100, 100), expected_sizes)
        
        
    def test_getSetEnabledModelsForType(self):
        tool = self.tool
        models = tool.listModels()
        self.failIf(len(models) == 0, "No models registered, aborting test %s")

        tmpl_ids = [m.id for m in models]
        tmpl_ids.sort()
        tool.setEnabledModelsForType('PloneArticle', tmpl_ids, tmpl_ids[0])
        availables, default = tool.getEnabledModelsForType('PloneArticle')
        availables = list(availables)
        self.assertEquals(availables, tmpl_ids)
        self.assertEquals(default, tmpl_ids[0])

        # setting a default view not listed in views should not raise exception
        exception_raised = True
        try:
            tool.setEnabledModelsForType('PloneArticle', tmpl_ids, 'dummy__')
            exception_raised = False
        except ValueError:
            pass
        self.failIf(exception_raised,
                    "Exception raised when setting a dummy default template "
                    "not listed in views")

    def test_cleanFilename(self):
        files = (
            ('C:\something\with spaces\windows name.txt', 'windows name.txt'),
            ('/the/unix naming/way/unix name.txt', 'unix name.txt')
            )

        for fullpath, expected in files:
            result = self.tool.cleanFilename(fullpath)
            self.assertEquals(result, expected)

    def testMigrationFinished(self):
        """Check version is correctly set after install"""
        t = self.tool
        self.assertEqual(t.getVersion(),
                         t.getVersionFromFS())

    def testNeedsVersionMigration(self):
        """No migration required immediately after install!"""
        t = self.tool
        self.failIf(
            t.needsVersionMigration(),
            'Tool needs upgrading, currently: %s, FS version: %s' % (
                str(t.getVersion()), t.getVersionFromFS()
                )
            )

        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(ArticleToolTestCase))
    return suite
            

