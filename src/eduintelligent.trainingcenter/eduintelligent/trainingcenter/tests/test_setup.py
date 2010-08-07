from base import TrainingCenterTestCase

class TestProductInstall(TrainingCenterTestCase):

    def afterSetUp(self):
        self.types = ('TrainingCenter', 'eduMember')

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
        self.failUnless('training_center_workflow' in workflowIds)
        self.failUnless('edumember_workflow' in workflowIds)
        
    def testWorkflowsMapped(self):
        wf = self.portal.portal_workflow
        self.assertEquals(('training_center_workflow',), wf.getChainForPortalType('TrainingCenter'))
        self.assertEquals(('edumember_workflow',), wf.getChainForPortalType('eduMember'))

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductInstall))
    return suite
