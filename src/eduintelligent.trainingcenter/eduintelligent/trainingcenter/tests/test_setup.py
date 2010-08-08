from base import TrainingCenterTestCase

from Products.membrane.interfaces import ICategoryMapper
from Products.membrane.config import ACTIVE_STATUS_CATEGORY
from Products.membrane.utils import generateCategorySetIdForType

class TestProductInstall(TrainingCenterTestCase):

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
        
    def testMembraneActiveWorkflowMappingForEmployee(self):
        states = { 'Department' : ['active',],
                   'Employee'   : ['active',],
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

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductInstall))
    return suite
