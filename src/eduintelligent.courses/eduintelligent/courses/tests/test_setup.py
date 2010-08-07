from base import CoursesTestCase

class TestProductInstall(CoursesTestCase):

    def afterSetUp(self):
        self.types = ('Course Folder', 'Course', 'Lessons', 'CourseContent', 'Resources', 'ExamContent', 'QuizContent', 'PollContent')

    def testTypesInstalled(self):
        for t in self.types:
            self.failUnless(t in self.portal.portal_types.objectIds(),
                            '%s content type not installed' % t)
    
    def testPortalFactoryEnabled(self):
        for t in self.types:
            import pdb; pdb.set_trace()
            self.failUnless(t in self.portal.portal_factory.getFactoryTypes().keys(),
                            '%s content type not installed' % t)
        
    def testWorkflowsInstalled(self):
        workflowIds = self.portal.portal_workflow.objectIds()
        self.failUnless('educourses_workflow' in workflowIds)
        
    def testWorkflowsMapped(self):
        wf = self.portal.portal_workflow
        self.assertEquals(('educourses_workflow',), wf.getChainForPortalType('Course'))
        self.assertEquals(('educourses_workflow',), wf.getChainForPortalType('Lessons'))

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductInstall))
    return suite
