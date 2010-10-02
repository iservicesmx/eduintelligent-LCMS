import unittest

from eduintelligent.policy.tests.base import EduIntelligentPolicyTestCase

class TestSetup(EduIntelligentPolicyTestCase):
    def test_portal_title(self):
        self.assertEquals('Plone site', self.portal.getProperty('title'))
        
    def test_portal_description(self):
        self.assertEquals('', self.portal.getProperty('description'))
        
def test_suite():
    suite= unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite

