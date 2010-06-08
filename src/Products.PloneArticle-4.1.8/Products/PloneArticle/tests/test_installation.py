# -*- coding: utf-8 -*-
## Test case for PloneArticle Install procedure
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
Test case for PloneArticle Install procedure
"""

__docformat__ = 'restructuredtext'

# Zope
from zope.component import getUtility
from zope.app.publisher.interfaces.browser import IBrowserMenu

#CMF
from Products.CMFCore.utils import getToolByName

from Products.PloneTestCase.setup import PLONE25, PLONE30

# Products imports
from Products.PloneArticle.tests.common import BaseTestCase
from Products.PloneArticle.config import PLONEARTICLE_TOOL

class TestInstallation(BaseTestCase):
    """
    """

    def afterSetUp(self):
        self.qi = getToolByName(self.portal, 'portal_quickinstaller')
        self.ttool = getToolByName(self.portal, 'portal_types')
        self.wf = getToolByName(self.portal, 'portal_workflow')
        # As ZopeTestCase REQUEST has no 'PARENTS', PlacelessTranslationService
        # raises a KeyError and cannot translate. This is an (ugly) workaround.
        self.app.REQUEST.set('PARENTS', [self.portal, self.app])
        return

    def test_installedAllTypes(self):
        """ test types installed """
        ttool = self.ttool
        installed_types = tids = ttool.objectIds()

        to_install = ('PloneArticle', 'FileInnerContentProxy',
                      'ImageInnerContentProxy', 'LinkInnerContentProxy',)

        not_to_install = ('BaseInnerContentProxy',)

        for tid in to_install:
            self.failUnless(tid in installed_types,
                            '%s is not installed' % tid,)
            tinfo = ttool[tid]
            self.failUnless(tinfo.product == 'PloneArticle', tinfo.product)

        for tid in not_to_install:
            self.failIf(tid in installed_types, '%s is installed' % tid)

    def testWorkflowChains(self):

        default_chain = ('simple_publication_workflow',)
        mapping = {
            'PloneArticle': default_chain,
            'FileInnerContentProxy': (),
            'ImageInnerContentProxy': (),
            'LinkInnerContentProxy': (),
            'InnerContentContainer': (),
            'PloneArticleTool': (),
            }

        for pt, wf in mapping.items():
            pwf = self.wf.getChainFor(pt)
            self.failUnlessEqual(pwf, wf, (pt, pwf, wf))

    def test_skin_installed(self):
        stool = getToolByName(self.portal, 'portal_skins')
        ids = stool.objectIds()
        self.failUnless('plonearticle' in ids,
                        "'plonearticle' not found in portal_skins")

    def testToolInstalled(self):
        atool = getToolByName(self.portal, PLONEARTICLE_TOOL)
        self.failUnless(atool is not None)

    def testGetAddableTypesInMenu(self):
        self.loginAsPortalOwner()
        addable_type_ids = (
            'PloneArticle',)
        not_addable_type_ids = (
            'FileInnerContentProxy',
            'ImageInnerContentProxy',
            'LinkInnerContentProxy',
            'InnerContentContainer',
            'PloneArticleTool',
            )
        allowed_types = self.portal.getAllowedTypes()
        allowed_type_ids = [x.getId() for x in allowed_types]
        self.failUnless(len([x for x in addable_type_ids if x in allowed_type_ids]) == len(addable_type_ids))
        self.failUnless([x for x in not_addable_type_ids if x not in allowed_type_ids])
        menu_types = getUtility(IBrowserMenu, name='plone_contentmenu_factory', context=self.folder)
        menu_types = menu_types.getMenuItems(self.portal, self.app.REQUEST)
        menu_type_ids = [x['extra']['id'] for x in menu_types]
        self.failUnless(len([x for x in addable_type_ids if x.lower() in menu_type_ids]), len(addable_type_ids))
        self.failUnless([x for x in not_addable_type_ids if x.lower() not in menu_type_ids])
        self.logout()

    def testTypesNotSearched(self):
        test_type_ids = (
            'FileInnerContentProxy',
            'ImageInnerContentProxy',
            'LinkInnerContentProxy',
            'InnerContentContainer',
            'PloneArticleTool',
            )
        ptool = getToolByName(self.portal, 'portal_properties')
        types_not_searched = ptool.site_properties.types_not_searched
        self.failUnless(len([x for x in test_type_ids if x in types_not_searched]) == len(test_type_ids))

    def testTypesNotToList(self):
        test_type_ids = (
            'FileInnerContentProxy',
            'ImageInnerContentProxy',
            'LinkInnerContentProxy',
            'InnerContentContainer',
            'PloneArticleTool',
            )
        ptool = getToolByName(self.portal, 'portal_properties')
        types_not_to_list = ptool.navtree_properties.metaTypesNotToList
        self.failUnless(len([x for x in test_type_ids if x in types_not_to_list]) == len(test_type_ids))

    def testKupuConfiguration(self):

        ktool = getToolByName(self.portal, 'kupu_library_tool')
        self.failUnless('FileInnerContentProxy' in ktool.getPortalTypesForResourceType('linkable'))
        self.failUnless('PloneArticle' in ktool.getPortalTypesForResourceType('collection'))
        self.failUnless('InnerContentContainer' in ktool.getPortalTypesForResourceType('collection'))
        self.failUnless('ImageInnerContentProxy' in ktool.getPortalTypesForResourceType('mediaobject'))

    def testPortalFactoryConfiguration(self):

        ftool = getToolByName(self.portal, 'portal_factory')
        types = ftool.getFactoryTypes()
        self.failUnless('PloneArticle' in types)
        self.failUnless('FileInnerContentProxy' in types)
        self.failUnless('ImageInnerContentProxy' in types)
        self.failUnless('LinkInnerContentProxy' in types)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstallation))
    return suite
