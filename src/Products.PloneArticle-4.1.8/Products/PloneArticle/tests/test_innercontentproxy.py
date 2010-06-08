# -*- coding: utf-8 -*-
## Test case for all InnerContentProxy classes
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

# Python imports
from types import TupleType

# Zope imports
from zope.interface import Interface

# CMF imports
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.tests.utils import mkDummyInContext
from Products.Archetypes.tests.test_fields import Dummy
from Products.Archetypes.public import Schema, FileField, ImageField, \
    StringField, BaseContent

# Products imports
from Products.PloneArticle.tests.common import BaseTestCase, openTestFile, \
     loadFile
from Products.PloneArticle import proxy as pa_proxies
from Products.PloneArticle.field import InnerContentContainer

from Products.CMFPlone.utils import _createObjectByType

test_types_names = [
    'BaseInnerContentProxy',
    'FileInnerContentProxy',
    'ImageInnerContentProxy',
    'LinkInnerContentProxy',
    ]

schema = Schema((
   FileField('file'),
   ImageField('image'),
   StringField('remoteUrl'),
   ),)

test_proxies = (
    ('file', 'FileInnerContentProxy',),
    ('image', 'ImageInnerContentProxy',),
    ('link', 'LinkInnerContentProxy',),
    )

class FieldData:

    def __init__(self, proxy_name, primary_field_name,
                 attached_name, attached_value, attached_expected,
                 ref_type, ref_value, ref_expected,
                 default):

        self.proxy_name = proxy_name
        self.primary_field_name = primary_field_name
        self.attached_name = attached_name
        self.attached_value = attached_value
        self.attached_expected = attached_expected
        self.ref_type = ref_type
        self.ref_value = ref_value
        self.ref_expected = ref_expected
        self.default = default

test_primary_fields = (
    FieldData('file', 'file',
              'attachedFile', 'attached file', 'attached file',
              'File', 'ref file', 'ref file',
              ''),
    FieldData('image', 'image',
              'attachedImage', loadFile('test.gif'), loadFile('test.gif'),
              'Image', loadFile('test.jpg'), loadFile('test.jpg'),
              ''),
    FieldData('link', 'remoteUrl',
              'attachedLink', 'attached link', 'attached link',
              'Link', 'ref link', 'http://nohost/plone/link',
              ''),
    )

file_proxy_values = (
    {'id': 'object_1',
     'title': 'Title 1',
     },
    {'id': 'object_2',
     'title': 'Title 2',
     },
    )


class InnerContentProxyTestCase(BaseTestCase):
    """
    Test all our inner content proxies
    """

    def afterSetUp(self):
        self.setRoles(['Manager'])
        self.article = self.addPloneArticle(self.portal, 'article')
        name = 'proxies'
        self.proxies = InnerContentContainer(name)
        self.proxies = self.proxies.__of__(self.portal)
        self.portal._setObject(name, self.proxies)
        for name, portal_type in test_proxies:
            self.proxies.invokeFactory(type_name=portal_type, id=name)

    def testGetPrimaryValue(self):
        self.loginAsPortalOwner()

        #for name, attached_name, attached_value, ref_type, ref_value, default in test_primary_fields:
        for data in test_primary_fields:

            proxy = self.proxies[data.proxy_name]
            primary_field = proxy.getField(data.primary_field_name)
            primary_accessor = primary_field.getAccessor(proxy)

            # Create referenced content
            kwargs = {}
            kwargs[data.primary_field_name] = data.ref_value
            ref_content = self.addContent(data.ref_type, self.portal,
                                          data.proxy_name)
            ref_content.edit(**kwargs)

            # No referenced content, no attached file
            value = primary_accessor()
            self.assertEquals(getattr(value, 'data', value), data.default)

            # Referenced content, no attached file
            kwargs = {}
            kwargs['referencedContent'] = (ref_content.UID(),)
            proxy.edit(**kwargs)
            value = primary_accessor()
            self.assertEquals(getattr(value, 'data', value), data.ref_expected)

            # referenced content, attached file
            kwargs = {}
            kwargs[data.attached_name] = data.attached_value
            proxy.edit(**kwargs)
            value = primary_accessor()
            self.assertEquals(getattr(value, 'data', value),
                              data.attached_expected)

            # No Referenced content, attached file
            kwargs = {}
            kwargs['referencedContent'] = ()
            value = primary_accessor()
            self.assertEquals(getattr(value, 'data', value), data.attached_expected)

        self.logout()

    def testReferenceableInterfaces(self):

        for class_name in test_types_names:
            klass = getattr(pa_proxies, class_name)
            rf_present = hasattr(klass, 'referenceable_interfaces')
            if class_name == 'BaseInnerContentProxy':
                self.failIf(rf_present,
                            "BaseInnerContentProxy must not define 'referenceable_interfaces'")
            else:
                self.failIf(not rf_present, "%s must define 'referenceable_interfaces'" % class_name)
                attr = getattr(klass, 'referenceable_interfaces')
                is_tuple = type(attr) == TupleType
                self.failUnless(is_tuple, "%s.referenceable_interfaces is not a tuple" % class_name)

                if is_tuple:
                    for i in attr:
                        self.failUnless(issubclass(i, Interface),
                            "%s.referenceable_interfaces: %s is not an interface" % (class_name, i.__name__))

    def testgetReferenceablePortalTypes(self):
        article = self.article
        article.setFiles(file_proxy_values)
        fp = article.getFiles()[0]
        rpt = fp.getReferenceablePortalTypes(article.getField('files'))
        self.assertEquals(rpt, ['File'])

    def testRenameAfterCreation(self):
        fields_data = (
            ('LinkInnerContentProxy',
             {'title': 'My nice title',}, 'my-nice-title',
             ),
            ('ImageInnerContentProxy',
             {'title': 'Test renamed after file name',
              'attachedImage_file': openTestFile('test.jpg'),
              },
             'test.jpg'),
            ('ImageInnerContentProxy',
             {'title': 'Test twice the same file name',
              'attachedImage_file': openTestFile('test.jpg'),
              },
             'test-1.jpg'),
            ('FileInnerContentProxy',
             {'title': 'Test file renamed after file name',
              'attachedFile_file': openTestFile('test.jpg'),
              },
             'test-2.jpg'),
            )

        self.loginAsPortalOwner()

        # from http://www.zope.org/Members/shh/ZopeTestCaseWiki/FrequentlyAskedQuestions
        # ensure we have _p_jar to avoid problems with CopySupport (cb_isMoveable)
        import transaction
        transaction.savepoint(optimistic=True)

        for ptype, data, expected_id in fields_data:
            initial_id = self.portal.generateUniqueId(ptype)
            proxy_id = self.proxies.invokeFactory(ptype, initial_id)
            proxy = self.proxies[proxy_id]
            proxy.processForm(values=data)

            self.assertEquals(proxy.getId(), expected_id)

    def test_searcheableText(self):
        """ test circular reference in linkinnerproxy """
        self.loginAsPortalOwner()

        ## article1 reference article2
        article1 = self.article
        article2 = self.addPloneArticle(self.portal, 'article2')
        _createObjectByType('InnerContentContainer',article1,'links')
        _createObjectByType('LinkInnerContentProxy',article1.links, 'link')
        article1.links.link.update(title='Reference to article 2',
                                            description='description2',
                                            referencedContent=article2)
        ## article2 reference artilce1
        _createObjectByType('InnerContentContainer',article2,'links')
        _createObjectByType('LinkInnerContentProxy',article2.links, 'link')
        article2.links.link.update(title='Reference to article 1',
                                    description='description1',
                                    referencedContent=article1)
        self.failUnless('Reference to article 2' in article1.SearchableText() )
        self.failUnless('Reference to article 1' in article2.SearchableText() )





def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(InnerContentProxyTestCase))
    return suite

