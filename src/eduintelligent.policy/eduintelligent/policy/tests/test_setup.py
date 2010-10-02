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

class TestCourses(EduIntelligentPolicyTestCase):

    def afterSetUp(self):
        self.types = ('Course Folder', 'Course', 'Lessons', 'CourseContent', 'Resources', 'ExamContent', 'QuizContent', 'PollContent')

    def testTypesInstalled(self):
        for t in self.types:
            self.failUnless(t in self.portal.portal_types.objectIds(),
                            '%s content type not installed' % t)
    
    def testPortalFactoryEnabled(self):
        for t in self.types:
            self.failUnless(t in self.portal.portal_factory.getFactoryTypes().keys(),
                            '%s content type not installed' % t)
        
    def testWorkflowsInstalled(self):
        workflowIds = self.portal.portal_workflow.objectIds()
        self.failUnless('educourses_workflow' in workflowIds)
        
    def testWorkflowsMapped(self):
        wf = self.portal.portal_workflow
        self.assertEquals(('educourses_workflow',), wf.getChainForPortalType('Course'))
        self.assertEquals(('educourses_workflow',), wf.getChainForPortalType('Lessons'))

from Products.membrane.interfaces import ICategoryMapper
from Products.membrane.config import ACTIVE_STATUS_CATEGORY
from Products.membrane.utils import generateCategorySetIdForType

class TestTrainingCenter(EduIntelligentPolicyTestCase):

    def afterSetUp(self):
        self.types = ('TrainingCenter', 'eduMember')

    def testTypesInstalled(self):
        for t in self.types:
            self.failUnless(t in self.portal.portal_types.objectIds(),
                            '%s content type not installed' % t)

    def testTypesRegisteredWithMembrane(self):
        for t in self.types:
            self.failUnless(t in self.portal.membrane_tool.listMembraneTypes(),
                            '%s content type not added to membrane' % t)
        
    def testMembraneActiveWorkflowMapping(self):
        states = { 'TrainingCenter' : ['active', 'inactive'],
                   'eduMember'      : ['active', 'inactive'],
                   }
        categoryMap = ICategoryMapper(self.portal.membrane_tool)
        for t, s in states.items():
            categorySet = generateCategorySetIdForType(t)
            self.assertEquals(s, categoryMap.listCategoryValues(categorySet, ACTIVE_STATUS_CATEGORY))
    
    def testPortalFactoryEnabled(self):
        for t in self.types:
            self.failUnless(t in self.portal.portal_factory.getFactoryTypes().keys(),
                            '%s content type not installed' % t)
        
    def testWorkflowsInstalled(self):
        workflowIds = self.portal.portal_workflow.objectIds()
        self.failUnless('training_center_workflow' in workflowIds)
        self.failUnless('edumember_workflow' in workflowIds)
        
    def testWorkflowsMapped(self):
        wf = self.portal.portal_workflow
        self.assertEquals(('training_center_workflow',), wf.getChainForPortalType('TrainingCenter'))
        self.assertEquals(('edumember_workflow',), wf.getChainForPortalType('eduMember'))

class TestEvaluation(EduIntelligentPolicyTestCase):

    def afterSetUp(self):
        self.types = ('Exam', 'Quiz', 'QuestionFillIn', 'QuestionChoice')

    def testTypesInstalled(self):
        for t in self.types:
            self.failUnless(t in self.portal.portal_types.objectIds(),
                            '%s content type not installed' % t)
    
    def testPortalFactoryEnabled(self):
        for t in self.types:
            self.failUnless(t in self.portal.portal_factory.getFactoryTypes().keys(),
                            '%s content type not installed' % t)

def test_suite():
    suite= unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    suite.addTest(unittest.makeSuite(TestCourses))
    suite.addTest(unittest.makeSuite(TestTrainingCenter))
    suite.addTest(unittest.makeSuite(TestEvaluation))
    return suite

