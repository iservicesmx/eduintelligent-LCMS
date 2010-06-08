# -*- coding: utf-8 -*-
## Test case for all InnerContentWidget classes
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
Test case for all InnerContentWidget classes
"""

__docformat__ = 'restructuredtext'

# Products imports
from Products.PloneArticle.tests.common import BaseTestCase

test_fieldnames = ('files', 'images', 'links',)

form = {
    'files_innercontent000000_id': 'file_1',
    'files_innercontent000000_title': 'File 1',
    'files_innercontent000001_id': 'file_2',
    'files_innercontent000001_title': 'File 2',
    'files_innercontent_position': ('000000', '000001'),
    'images_innercontent000000_id': 'image_1',
    'images_innercontent000000_title': 'Image 1',
    'images_innercontent_position': ('000000',),
    'links_innercontent000000_id': 'link_1',
    'links_innercontent000000_title': 'Link 1',
    'links_innercontent000001_id': 'link_2',
    'links_innercontent000001_title': 'Link 2',
    'links_innercontent_position': ('000001', '000000'),
}

expected_values = {
    'files': (
        (
            {'id': ('file_1', {}),
             'title': ('File 1', {}),
             },
            {'id': ('file_2', {}),
             'title': ('File 2', {}),
             },
        ), 
        {},
    ),
    'images': (
        (
            {'id': ('image_1', {}),
             'title': ('Image 1', {}),
             },
        ), 
        {},
    ),
    'links': (
        (
            {'id': ('link_2', {}),
             'title': ('Link 2', {}),
             },
            {'id': ('link_1', {}),
             'title': ('Link 1', {}),
             },
        ), 
        {},
    ),
}

tests = []

class InnerContentWidgetTestCase(BaseTestCase):
    """
    This class contains all test cases for all InnerContentWidget classes
    """

    def afterSetUp(self):
        """ """
        self.loginAsPortalOwner()
        self.article = self.addPloneArticle(self.portal, 'article')
        self.logout()
        
    def test_processing(self):
        """ """
        article = self.article
        
        for name in test_fieldnames:
            field = article.getField(name)
            widget = field.widget
            value = widget.process_form(article, field, form)
            expected_value = expected_values[name]
            self.assertEquals(len(value), 2)
            self.assertEquals(value[1], expected_value[1])
            
            # Test dictionnaries, so test each key
            items = value[0]
            expected_items = expected_value[0]
            self.assertEquals(len(items), len(expected_items))
            for index in range(0, len(items)):
                result_items = items[index].items()
                result_items.sort()
                expected = expected_items[index].items()
                expected.sort()
                self.assertEquals(result_items, expected)

    def testMakeWidgetId(self):
        """"""
        article = self.article
        field = article.getField('images')
        widget = field.widget

        expected = 'myFieldName-innercontent000042'
        result = widget.makeWidgetId('myFieldName', 42)
        self.assertEqual(result, expected)

    def testWidgetFieldAssocs(self):
        assocs = (
            ('FileInnerContentField', 'FileInnerContentWidget'),
            ('ImageInnerContentField', 'ImageInnerContentWidget'),
            ('LinkInnerContentField', 'LinkInnerContentWidget'),
            )

        product = 'Products.PloneArticle.'

        from Products.Archetypes.Registry import fieldDescriptionRegistry
        from Products.Archetypes.Registry import widgetDescriptionRegistry
        
        for field, widget in assocs:
            module = field[:-5].lower()
            field_path = product + 'field.' + module + '.' + field
            desc = fieldDescriptionRegistry.get(field_path, None)
            self.failIf(desc is None, "%s is not registered" % field_path)

            widget_path = product + 'widget.' + module + '.' + widget
            self.assert_(
                widgetDescriptionRegistry.get(widget_path, None) is not None,
                "Widget %s is not properly registered" % widget
                )
            self.assert_(widget_path in desc.allowed_widgets(),
                        "Widget %s is not listed in allowed_widget for %s"
                        % (widget_path, field_path))
            
tests.append(InnerContentWidgetTestCase)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    for test in tests:
        suite.addTest(makeSuite(test))
    return suite
