from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

ztc.installProduct('membrane')

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_eduintelligent_training():
    """Set up the additional products required for the EduIntelligent Training Center.
    
    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
    
    fiveconfigure.debug_mode = True
    import eduintelligent.trainingcenter
    zcml.load_config('configure.zcml', eduintelligent.trainingcenter)
    fiveconfigure.debug_mode = False

    ztc.installPackage('eduintelligent.trainingcenter')
    
setup_eduintelligent_training()
ptc.setupPloneSite(products=['membrane', 'eduintelligent.trainingcenter'])

class TrainingCenterTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here. This applies to unit 
    test cases.
    """

class TrainingCenterFunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use doctest
    syntax. Again, we can put basic common utility or setup code in here.
    """
