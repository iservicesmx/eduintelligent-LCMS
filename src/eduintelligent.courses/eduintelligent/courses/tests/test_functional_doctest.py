"""This is a a functional doctest test. It uses PloneTestCase and doctest
syntax. In the test itself, we use zope.testbrowser to test end-to-end
functionality, including the UI.

One important thing to note: zope.testbrowser is not JavaScript aware! For
that, you need a real browser. Look at zope.testbrowser.real and Selenium
if you require "real" browser testing.
"""

import unittest
import doctest


from Testing import ZopeTestCase as ztc

from eduintelligent.courses.tests import base

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    return unittest.TestSuite([

        # Here, we create a test suite passing the name of a file relative 
        # to the package home, the name of the package, and the test base 
        # class to use. Here, the base class is a full PloneTestCase, which
        # means that we get a full Plone site set up.

        # The actual test is in functional.txt

        ztc.ZopeDocFileSuite(
            'tests/functional_tests.txt', package='eduintelligent.courses',
            test_class=base.CoursesFunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
            
        # We could add more doctest files here as well, by copying the file
        # block above.

        ])
