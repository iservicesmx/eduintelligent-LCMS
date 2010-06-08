# Copyright (c) 2003-2006 Ingeniweb SAS

# This software is subject to the provisions of the GNU General Public
# License, Version 2.0 (GPL).  A copy of the GPL should accompany this
# distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY,
# AGAINST INFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE

# More details in the ``LICENSE`` file included in this package.

"""
Test case for PloneArticle content type
"""

__docformat__ = 'restructuredtext'

import os
from Acquisition import Implicit
from Globals import package_home

# Products imports
from Products.PloneArticle.config import GLOBALS
from Products.PloneArticle.tests.common import BaseTestCase


class TestMigration(BaseTestCase):

    def importArticleV3(self, container):
        """
            Import article V3 from zexp
        """
        
        article_id = 'articlev3'
        zexp_path = os.path.join(package_home(GLOBALS), 'tests', '%s.zexp' % article_id)
        container._importObjectFromFile(zexp_path, verify = 1, set_owner = 1)
        return getattr(container, article_id)

    def testPloneArticleMigrationV3ToV4(self):
        self.loginAsPortalOwner()
        
        # Import article in v2.x
        article = self.importArticleV3(self.portal)
        article.reindexObject()
        article_id = article.getId()
        
        # Attributes before migration
        ### XXX for tests, this value have to be really hardcoded
        article_id = article.getId()
        article_title = article.Title()
        article_description = article.Description()
        article_text = article.getText()
        
        self.failUnless(hasattr(article, '__ordered_attachment_refs__'))
        self.failUnless(hasattr(article, '__ordered_image_refs__'))
        self.failUnless(hasattr(article, '__ordered_link_refs__'))
        
        
        # Migrate to 4
        Migrator().migrate(self.portal)
        
        # Attributes after migration
        ### XXX check that all is allright.
        self.logout()

class TestMigrationPath(BaseTestCase):
    """The path to the actual version should exist"""

    def testMigrationPath(self):

        from Products.CMFCore.utils import getToolByName
        from Products.PloneArticle.config import PLONEARTICLE_TOOL
        from Products.PloneArticle.tool import _upgradePaths

        pa_tool = getToolByName(self.portal, PLONEARTICLE_TOOL)
        version_info = pa_tool.getVersionFromFS()
        new_versions = [x[0] for x in _upgradePaths.values()]
        self.failUnless(
            version_info[1] in new_versions,
            "No migrator found for version '%s'. Please correct migration/__init__.py\n"
            "You might consider this as a warning if you're not testing a released version"
            % version_info[1])
        return

#FIXME: this is just a non-functionnal skeleton of a test, don't expect it to
#pass. For now we will just return an empty test suite. Too bad.
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    # Uncomment below line to perform the migration test
    #suite.addTest(makeSuite(TestMigration))
    suite.addTest(makeSuite(TestMigrationPath))
    return suite
