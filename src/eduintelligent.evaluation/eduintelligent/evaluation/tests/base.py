from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_eduintelligent_evaluation():
    """Set up the additional products required for the EduIntelligent evaluations.
    
    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
  
    fiveconfigure.debug_mode = True
    import eduintelligent.evaluation
    zcml.load_config('configure.zcml', eduintelligent.evaluation)
    fiveconfigure.debug_mode = False

    ztc.installPackage('eduintelligent.evaluation')
    
setup_eduintelligent_evaluation()
ptc.setupPloneSite(products=['eduintelligent.evaluation'])

class EvaluationTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here. This applies to unit 
    test cases.
    """

class EvaluationFunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use doctest
    syntax. Again, we can put basic common utility or setup code in here.
    """
