# -*- coding: utf-8 -*-
## Test case for SmartListField
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
Test case for SmartListField
"""

__docformat__ = 'restructuredtext'

# Python imports
from copy import deepcopy
from types import ListType
from StringIO import StringIO

# CMF imports
from Products.CMFCore.utils import getToolByName

from Products.PloneTestCase.setup import PLONE21, PLONE25, PLONE30

# Archetypes imports
from Products.Archetypes.tests.utils import mkDummyInContext, makeContent
from Products.Archetypes.tests.test_fields import Dummy, FakeRequest
from Products.Archetypes.atapi import Schema
from Products.Archetypes.Registry import fieldDescriptionRegistry
from Products.Archetypes.Extensions.utils import installTypes
from Products.Archetypes.atapi import listTypes

# Products imports
from Products.PloneArticle.tests.common import BaseTestCase, loadFile
from Products.PloneArticle.field import SmartListField
from Products.PloneArticle import proxy as pa_proxies
from Products.PloneArticle.config import PROJECTNAME

def lowcase_cmp(s1, s2):
    return cmp(s1.lower(), s2.lower())

if PLONE30:
    ALL_ALLOWED_CRITERIAS= (
        'allowedRolesAndUsers', 'Creator', 'getEventType', 'getId',
        'getObjPositionInParent', 'getRawRelatedItems', 'id', 'in_reply_to',
        'is_default_page', 'is_folderish', 'meta_type', 'object_provides',
        'path', 'portal_type', 'review_state', 'SearchableText',
        'sortable_title', 'Subject', 'Type', 'UID'
        )
elif PLONE25:
    ALL_ALLOWED_CRITERIAS = (
        'allowedRolesAndUsers', 'Creator', 'getEventType', 'getId',
        'getObjPositionInParent', 'getRawRelatedItems', 'id', 'in_reply_to',
        'is_default_page', 'is_folderish', 'meta_type', 'path', 'portal_type',
        'review_state', 'SearchableText', 'sortable_title', 'Subject', 'Type'
        )
else: # Plone 2.1 ?
    ALL_ALLOWED_CRITERIAS = (
        'allowedRolesAndUsers', 'Creator', 'getId',
        'getObjPositionInParent', 'getRawRelatedItems', 'id', 'in_reply_to',
        'is_default_page', 'is_folderish', 'meta_type', 'path', 'portal_type',
        'review_state', 'SearchableText', 'sortable_title', 'Subject', 'Type')

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


class SmartListFieldTestCase(BaseTestCase):
    """
    """

    def afterSetUp(self):
        self.setRoles(['Manager'])
        self._dummy = mkDummyInContext(Dummy, oid='dummy',
                                       context=self.portal,
                                       schema=schema)
        self.article = makeContent(self.portal, 'PloneArticle', id='article')
        typeInfo = [ti for ti in listTypes(PROJECTNAME) if ti['name'] == 'SimpleSmartContent']
        dummy_out = StringIO()
        installTypes(self.portal, dummy_out, typeInfo, PROJECTNAME)



    def makeDummy(self):
        return self._dummy

    def testField_registered(self):
        self.failUnless(
            fieldDescriptionRegistry.get(
                'Products.PloneArticle.field.smartlist.SmartListField', None),
            "SmartListField is not registered by archetypes")

    def testAlwaysMultiValued(self):
        self.failUnless(SmartListField(multiValued=False).multiValued,
                        'Field does not enforce multivalued to True')

    def testAllowedTypes(self,):
        dummy = self.makeDummy()
        field = dummy.getField('smartlistfield')
        site_props = self.portal.portal_properties.site_properties
        types_not_searched = site_props.types_not_searched

        not_allowed_types = [t for t in field.getAllowedTypes(dummy)
                             if t in types_not_searched]
        self.failIf(not_allowed_types,
                    "Field allow to reference content normally excluded from search: %s"
                    % repr(not_allowed_types))

        restricted_field = dummy.getField('restricted_smartlistfield')
        self.assertEquals(restricted_field.getAllowedTypes(dummy),
                          ['PloneArticle',])

    def testAllowedCriterias(self):
        dummy = self.makeDummy()
        field = dummy.getField('restricted_smartlistfield')

        all_criterias = list(ALLOWED_CRITERIAS)
        all_criterias.sort(lowcase_cmp)
        self.assertEquals(field.getAllowedCriterias(dummy),
                          tuple(all_criterias))

        field = dummy.getField('smartlistfield')
        ct = getToolByName(self.portal, 'portal_catalog')

        self.assertEquals(field.getAllowedCriterias(dummy),
                          ALL_ALLOWED_CRITERIAS)

    def testGetSetSearchCriteria(self):
        empty_search = {'SearchableText': '', 'portal_types': (),}
        invalid_search = empty_search.copy()
        invalid_search.update({'invalid_index': False})

        dummy = self.makeDummy()
        field = dummy.getField('smartlistfield')

        # type checking
        self.assertRaises(TypeError, field.setSearchCriterias, dummy, None)

        # identity
        field.setSearchCriterias(dummy, empty_search)
        field_search = field.getSearchCriterias(dummy)
        self.failIf(empty_search != field_search)

        # invalid search keys must be discarded
        # we need to copy dict, mutator will change it
        field.setSearchCriterias(dummy, invalid_search.copy())
        field_search = field.getSearchCriterias(dummy)
        self.failIf(field_search == invalid_search)
        self.failIf(field_search != empty_search)

    def testGetSetAutoReference(self):
        dummy = self.makeDummy()
        field = dummy.getField('smartlistfield')

        self.assertEquals(field.getAutoReference(dummy), True)
        field.setAutoReference(dummy, False)
        self.assertEquals(field.getAutoReference(dummy), False)

        # test default parameter
        field = dummy.getField('restricted_smartlistfield')
        self.assertEquals(field.getAutoReference(dummy), False)

    def testExcludedUIDS(self):
        dummy = self.makeDummy()
        field = dummy.getField('smartlistfield')

        excluded_uids = field.getExcludedUIDs(dummy)
        self.assertEquals(excluded_uids, {},
                          "Initials excluded_uids not empty: '%s'"
                          % repr(excluded_uids))

        # verify it will accept only dict
        self.assertRaises(TypeError, field.setExcludedUIDs,
                          field, dummy, ())

        EXCLUDED = {'1': True}
        field.setExcludedUIDs(dummy, EXCLUDED)
        excluded_uids = field.getExcludedUIDs(dummy)
        self.assertEquals(excluded_uids, EXCLUDED)

    def testSet(self):

        content = makeContent(self.portal, "SimpleSmartContent",
                              id="smartlist_content")
        content_uid = content.UID()
        field = content.getField('smartlistfield')

        uct = getToolByName(self.portal, 'uid_catalog')
        ALL_UIDS = [b.UID for b in uct.searchResults() if b.UID != content_uid]
        total = len(ALL_UIDS)

        UIDS = ALL_UIDS[:-3]
        self.assert_(len(UIDS) >=3)
        REF_UIDS = UIDS[:2]
        REF_UIDS.sort()
        EXCLUDED = dict.fromkeys(UIDS[2:], True)

        field.set(content, REF_UIDS, uids_found=UIDS)
        value = field.getRaw(content)
        value.sort()
        self.assertEquals(value, REF_UIDS)

        excluded_uids = field.getExcludedUIDs(content)
        self.assertEquals(excluded_uids, EXCLUDED)

        # test with a common element:
        # in the new refs and old excluded:
        # => not in new excluded, present in new value
        #
        # and one in old value and 'found_uids' but not NEW_REFS::
        # not in new value, present in new excluded
        #
        NEW_UIDS = EXCLUDED.keys()[:1] + ALL_UIDS[-3:] + REF_UIDS[:1]
        NEW_REFS = NEW_UIDS[:2]
        ALL_REFS = REF_UIDS[1:] + NEW_REFS

        NEW_EXCLUDED = {NEW_UIDS[2]: True, NEW_UIDS[3]: True,
                        REF_UIDS[0]: True}

        ALL_EXCLUDED = dict(EXCLUDED)
        ALL_EXCLUDED.update(NEW_EXCLUDED)
        del ALL_EXCLUDED[NEW_REFS[0]]

        NEW_REFS.sort()
        ALL_REFS.sort()

        field.set(content, NEW_REFS, uids_found=NEW_UIDS)
        new_value = field.getRaw(content)
        new_value.sort()
        self.assertEquals(new_value, ALL_REFS)

        excluded_uids = field.getExcludedUIDs(content)
        self.assertEquals(excluded_uids, ALL_EXCLUDED)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(SmartListFieldTestCase))
    return suite
