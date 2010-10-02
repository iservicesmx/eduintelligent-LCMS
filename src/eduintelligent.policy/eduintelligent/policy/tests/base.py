from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_eduintelligent_policy():
    """ Setup the additional products required for eduIntelligent.
    
    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer
    """
    
    #Load the ZCML configuration for the eduintelligent.policy package
    
    fiveconfigure.debug_mode = True
    import eduintelligent.policy
    zcml.load_config('configure.zcml',eduintelligent.policy)
    fiveconfigure.debug_mode = False
    
    #We need to tell the testing framework that these products 
    #should be available. This can't happen until after we have loaded
    #the ZCML
    
    ztc.installPackage('eduintelligent.policy')
    
# The order here is impotant: We first call the (deferred) function
# which installs the products we need for the eduintelligent package. Then,
# we let PloneTestCase set up this product on installation.

setup_eduintelligent_policy()
ptc.setupPloneSite(products=['eduintelligent.policy'])

class EduIntelligentPolicyTestCase (ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If
    necessary, we can put common utility or setup code here.
    """

