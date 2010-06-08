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

# Products imports
from Products.PloneArticle.utils import find_classes_implementing_method
from Products.PloneArticle.tests.common import BaseTestCase

class FakeA:
    def dummy(self):
        pass
    
class FakeB:
    def dummy(self):
        pass
    
class FakeC(FakeA, FakeB):
    pass
    

class ArticleUtilsTestCase(BaseTestCase):
    """
    Test functions from utils package
    """
    
    def test_find_classes_implementing_method(self):
        expected_klasses = (FakeA, FakeB)
        klasses = find_classes_implementing_method(FakeC, 'dummy')
        self.assertEqual(expected_klasses, klasses)
    
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(ArticleUtilsTestCase))
    return suite
            

