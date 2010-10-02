import unittest

from eduintelligent.policy.tests.base import EduIntelligentPolicyTestCase

class TestSetup(EduIntelligentPolicyTestCase):
    def test_portal_title(self):
        self.assertEquals('eduIntelligent', self.portal.getProperty('title'))

    def test_portal_description(self):
        self.assertEquals('eduIntelligent Demo Site', self.portal.getProperty('description'))

    def test_portal_email_from_address(self):
        self.assertEquals('desarrollo@iservices.com.mx', self.portal.getProperty('email_from_address'))

    def test_portal_email_from_name(self):
        self.assertEquals('eduIntelligent', self.portal.getProperty('email_from_name'))

    def test_portal_validate_email(self):
        self.assertFalse(self.portal.getProperty('validate_email'))

    def test_portal_email_charset(self):
        self.assertEquals('utf-8', self.portal.getProperty('email_charset'))

    def test_portal_enable_permalink(self):
        self.assertTrue(self.portal.getProperty('enable_permalink'))

def test_suite():
    suite= unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite

