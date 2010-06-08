import unittest

from eduintelligent.policy.tests import EduIntelligentPolicyTestCase

class TestSetup(EduIntelligentPolicyTestCase):
    def test_portal_title(self):
        self.assertEquals("Plone", 
                          self.portal.getProperty('title'))
        
    def test_portal_description(self):
        self.assertEquals("Plone Description",
                          self.portal.getProperty('description'))
        
def test_suite():
    suite= unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite

