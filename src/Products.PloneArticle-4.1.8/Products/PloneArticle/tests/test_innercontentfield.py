# -*- coding: utf-8 -*-
## Test case for all InnerContentField classes
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
Test case for all InnerContentField classes
"""

__docformat__ = 'restructuredtext'

# Python imports
from copy import deepcopy
from types import ListType

# CMF imports
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.tests.utils import mkDummyInContext
from Products.Archetypes.tests.test_fields import FakeRequest
from Products.Archetypes.public import Schema, BaseFolderMixin

# Products imports
from Products.PloneArticle.tests.common import BaseTestCase, loadFile
from Products.PloneArticle import field as pa_fields
from Products.PloneArticle import proxy as pa_proxies

# we do as archetypes do for testing fields
test_fields = [
    ('FileInnerContentField', 'fileinnercontentfield'),
    ('ImageInnerContentField', 'imageinnercontentfield'),
    ('LinkInnerContentField', 'linkinnercontentfield'),
    ]

field_instances = []
for type_name, name in test_fields:
    field_instances.append(getattr(pa_fields, type_name)(name))

field_values = {
    'fileinnercontentfield': (
        {'id': 'object_1',
         'title': 'Title 1',
         },
        {'id': 'object_2',
         'title': 'Title 2',
         },
    ),
    'linkinnercontentfield': (
        {'id': 'object_1',
         'title': 'Title 1',
         },
        {'id': 'object_2',
         'title': 'Title 2',
         },
    ),
    'imageinnercontentfield': (
        {'id': 'object_1',
         'title': 'Title 1',
         },
        {'id': 'object_2',
         'title': 'Title 2',
         },
    ),
}

expected_values = {
    'fileinnercontentfield': (
        {'id': 'object_1',
         'title': 'Title 1',
         },
        {'id': 'object_2',
         'title': 'Title 2',
         },
    ),
    'imageinnercontentfield': (
        {'id': 'object_1',
         'title': 'Title 1',
         },
        {'id': 'object_2',
         'title': 'Title 2',
         },
    ),
    'linkinnercontentfield': (
        {'id': 'object_1',
         'title': 'Title 1',
         },
        {'id': 'object_2',
         'title': 'Title 2',
         },
    ),
}

empty_values = {
    'fileinnercontentfield': (),
    'imageinnercontentfield': (),
    'linkinnercontentfield': (),
    }

schema = Schema(tuple(field_instances))

proxy_classes = {
    'fileinnercontentfield': pa_proxies.FileInnerContentProxy,
    'imageinnercontentfield': pa_proxies.ImageInnerContentProxy,
    'linkinnercontentfield': pa_proxies.LinkInnerContentProxy,
    }

proxy_schemas = {
    'fileinnercontentfield': pa_proxies.FileInnerContentProxySchema,
    'imageinnercontentfield': pa_proxies.ImageInnerContentProxySchema,
    'linkinnercontentfield': pa_proxies.LinkInnerContentProxySchema,
    }

proxy_references =  (
    ('fileinnercontentfield', 'File', 'file', 'ref file', ),
    ('imageinnercontentfield', 'Image', 'image', loadFile('test.jpg'), ),
    ('linkinnercontentfield', 'Link', 'remoteUrl', 'http://www.google.fr', ),)

proxy_attached_field_names = (
    ('fileinnercontentfield', 'attachedFile'),
    ('imageinnercontentfield', 'attachedImage'),
    ('linkinnercontentfield', None),)

class Dummy(BaseFolderMixin):
    def Title(self):
        return 'Spam'

class InnerContentFieldTestCase(BaseTestCase):
    """
    This class contains all test cases for all InnerContentField classes
    """

    def afterSetUp(self):
        self.setRoles(['Manager'])
        self._dummy = mkDummyInContext(Dummy, oid='dummy', context=self.portal,
                                       schema=schema)

    def makeDummy(self):
        return self._dummy

    def test_processing(self):
        dummy = self.makeDummy()
        request = FakeRequest()
        request.form.update(field_values)
        dummy.REQUEST = request
        dummy.processForm(data=1)
        for k, v in expected_values.items():
            field = dummy.getField(k)
            got = dummy.getField(k).get(dummy)

            if isinstance(field, pa_fields.BaseInnerContentField):
                self.assertEquals(
                    type(got), ListType,
                    'Bad type for BaseInnerContentField: expected %s, got %s' % (ListType, type(got)))

                result_list = []
                for val in got:
                    self.failUnless(
                        isinstance(val, pa_proxies.BaseInnerContentProxy))
                    val = {'id': val.getId(), 'title': val.Title(),}
                    result_list.append(val)
                got = tuple(result_list)

            self.assertEquals(got, v, 'got: %r, expected: %r, field "%s"' %
                              (got, v, k))

    def test_inner_content_reorder(self):
        dummy = self.makeDummy()
        field_name = 'fileinnercontentfield'
        file_values = ({'id': 'reorder_object_1',
                        'title': 'Title 1',},
                       {'id': 'reorder_object_2',
                        'title': 'Title 2',
                        },)

        expected_values = ({'id': 'reorder_object_1',
                            'title': 'Title 1',},
                           {'id': 'reorder_object_2',
                            'title': 'Title 2',
                            },)

        field = dummy.getField(field_name)
        field.set(dummy, file_values)
        got = dummy.getField(field_name).get(dummy)

        result_list = []
        for val in got:
            val = {'id': val.getId(), 'title': val.Title(),}
            result_list.append(val)
        got = tuple(result_list)

        self.assertEquals(got, expected_values,
                          'error on set, cannot test reordering'
                          'got: %r, expected: %r, field "%s"' %
                          (got, expected_values, field_name))

        file_values = list(file_values)
        file_values.reverse()
        expected_values = list(expected_values)
        expected_values.reverse()
        field.set(dummy, file_values)
        got = dummy.getField(field_name).get(dummy)

        result_list = []
        for val in got:
            val = {'id': val.getId(), 'title': val.Title(),}
            result_list.append(val)
        got = result_list

        self.assertEquals(got, expected_values,
                          'field inner content reorder failed, '
                          'got: %r, expected: %r, field "%s"' %
                          (got, expected_values, field_name))

    def test_inner_content_update(self):
        dummy = self.makeDummy()
        field_name = 'fileinnercontentfield'
        file_values = ({'id': 'reorder_object_1',
                        'title': 'Title 1',},
                       {'id': 'reorder_object_2',
                        'title': 'Title 2',
                        },)

        expected_values = ({'id': 'reorder_object_1',
                            'title': 'Title 1',},
                           {'id': 'reorder_object_2',
                            'title': 'Title 2',
                            },)

        field = dummy.getField(field_name)
        field.set(dummy, file_values)
        got = dummy.getField(field_name).get(dummy)

        result_list = []
        for val in got:
            val = {'id': val.getId(), 'title': val.Title(),}
            result_list.append(val)
        got = tuple(result_list)

        self.assertEquals(got, expected_values,
                          'error on set, cannot test reordering'
                          'got: %r, expected: %r, field "%s"' %
                          (got, expected_values, field_name))

        update_values = ({'id': 'reorder_object_3',
                        'title': 'Title 3',},
                       {'id': 'reorder_object_4',
                        'title': 'Title 4',
                        },)

        expected_values = (
                           {'id': 'reorder_object_1',
                            'title': 'Title 1',},
                           {'id': 'reorder_object_2',
                            'title': 'Title 2',},
                           {'id': 'reorder_object_3',
                           'title': 'Title 3',},
                           {'id': 'reorder_object_4',
                            'title': 'Title 4',},)


        field.set(dummy, update_values, update=True)
        got = dummy.getField(field_name).get(dummy)

        result_list = []
        for val in got:
            val = {'id': val.getId(), 'title': val.Title(),}
            result_list.append(val)
        got = tuple(result_list)

        self.assertEquals(got, expected_values,
                          'error on set, cannot test reordering'
                          'got: %r, expected: %r, field "%s"' %
                          (got, expected_values, field_name))

        update_values = ({'id': 'reorder_object_3',
                        'title': 'Title 3.1',},)

        expected_values = (
                           {'id': 'reorder_object_1',
                            'title': 'Title 1',},
                           {'id': 'reorder_object_2',
                            'title': 'Title 2',},
                           {'id': 'reorder_object_3',
                           'title': 'Title 3.1',},
                           {'id': 'reorder_object_4',
                            'title': 'Title 4',},)


        field.set(dummy, update_values, update=True)
        got = dummy.getField(field_name).get(dummy)

        result_list = []
        for val in got:
            val = {'id': val.getId(), 'title': val.Title(),}
            result_list.append(val)
        got = tuple(result_list)

        self.assertEquals(got, expected_values,
                          'error on set, cannot test reordering'
                          'got: %r, expected: %r, field "%s"' %
                          (got, expected_values, field_name))

    def testPortalCatalog(self):
        dummy = self.makeDummy()
        ctool = getToolByName(self.portal, 'portal_catalog')
        for k, v in proxy_classes.items():
            field = dummy.getField(k)
            proxy_type = v.portal_type

            # Add proxies
            value = field_values[k]
            field.set(dummy, value)
            brains = ctool(portal_type=proxy_type)
            self.assertEquals(len(brains), 2)

            # Add the same proxies to make sure proxies are not duplicated
            field.set(dummy, value)
            brains = ctool(portal_type=proxy_type)
            self.assertEquals(len(brains), 2)

            # Delete proxies
            field.set(dummy, ())
            brains = ctool(portal_type=proxy_type)
            self.assertEquals(len(brains), 0)

            # Add temporary object
            brains = ctool(portal_type=proxy_type)
            brain_length = len(brains)
            tmp_obj = field.getTemporaryInnerContent(dummy)
            brains = ctool(portal_type=proxy_type)
            self.assertEquals(len(brains), brain_length)

    def testUIDCatalog(self):
        dummy = self.makeDummy()
        utool = getToolByName(self.portal, 'uid_catalog')
        for k, v in proxy_classes.items():
            field = dummy.getField(k)
            proxy_type = v.portal_type

            # Add proxies
            value = field_values[k]
            field.set(dummy, value)
            brains = utool(portal_type=proxy_type)
            self.assertEquals(len(brains), len(value))

            # Add the same proxies to make sure proxies are not duplicated
            field.set(dummy, value)
            brains = utool(portal_type=proxy_type)
            self.assertEquals(len(brains), len(value))

            # Delete proxies
            field.set(dummy, ())
            brains = utool(portal_type=proxy_type)
            self.assertEquals(len(brains), 0)

            # Add temporary object
            brains = utool(portal_type=proxy_type)
            brain_length = len(brains)
            tmp_obj = field.getTemporaryInnerContent(dummy)
            brains = utool(portal_type=proxy_type)
            self.assertEquals(len(brains), brain_length)

    def testReferenceCatalog(self):
        dummy = self.makeDummy()
        utool = getToolByName(self.portal, 'uid_catalog')
        rtool = getToolByName(self.portal, 'reference_catalog')
        for k, ref_type, ref_field, ref_value in proxy_references:
            field = dummy.getField(k)

            # Create referenced content
            kwargs = {}
            kwargs[ref_field] = ref_value
            ref_content = self.addContent(ref_type, self.portal, k)
            ref_content.edit(**kwargs)
            ref_content_uid = ref_content.UID()

            # Add proxies with a reference
            value = deepcopy(field_values[k])

            for item in value:
                item['referencedContent'] = ref_content_uid
            field.set(dummy, value)
            brains = utool(portal_type='Reference')
            self.assertEquals(len(brains), len(value))
            brains = rtool(targetUID=ref_content_uid)
            self.assertEquals(len(brains), len(value))


            # Add the same proxies to make sure proxies are not duplicated
            field.set(dummy, value)
            brains = utool(portal_type='Reference')
            self.assertEquals(len(brains), len(value))
            brains = rtool(targetUID=ref_content_uid)
            self.assertEquals(len(brains), len(value))

            # Delete proxies
            field.set(dummy, ())
            brains = utool(portal_type='Reference')
            self.assertEquals(len(brains), 0)

    def testGetTemporaryInnerContent(self):
        """Test field.BaseInnerContentField.getTemporaryInnerContent method"""
        dummy = self.makeDummy()
        for k, v in proxy_classes.items():
            field = dummy.getField(k)
            tmp_obj = field.getTemporaryInnerContent(dummy)
            self.failUnless(isinstance(tmp_obj, v))

    def testGetInnerContentSchema(self):
        """Test field.BaseInnerContentField.getInnerContentSchema method"""
        dummy = self.makeDummy()
        for k, v in proxy_schemas.items():
            field = dummy.getField(k)
            got_schema = field.getInnerContentSchema(dummy)
            self.assertEquals(got_schema, v)

    def testGetInnerContentAttachedField(self):
        """Test field.BaseInnerContentField.getInnerContentAttachedField"""
        dummy = self.makeDummy()
        for field_name, attached_name in proxy_attached_field_names:
            field = dummy.getField(field_name)
            result = field.getInnerContentAttachedField(dummy)
            if result is not None:
                result = result.getName()
            self.assertEquals(result, attached_name)

    def test_getIndexableValue(self):
        """Test if field returns the correct value for SearchableText index"""

        dummy = self.makeDummy()
        field_name = 'fileinnercontentfield'
        file_values = ({'id': 'object_1',
                        'title': 'Title 1',
                        'attachedFile': 'This is a dummy text'},
                       {'id': 'object_2',
                        'title': 'Title 2',
                        },)
        expected_value = "1 2 a dummy is text this title title"
        field = dummy.getField(field_name)
        field.set(dummy, file_values)
        value = field.getIndexableValue(dummy)
        value_list = [x.lower() for x in value.split(" ") if x]
        value_list.sort()
        value = " ".join(value_list)
        self.assertEquals(value, expected_value)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(InnerContentFieldTestCase))
    return suite
