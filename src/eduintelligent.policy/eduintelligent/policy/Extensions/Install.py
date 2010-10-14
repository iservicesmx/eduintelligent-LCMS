import transaction
from Products.CMFCore.utils import getToolByName

PRODUCT_DEPENDENCIES = ('membrane',
                        'remember',
                        'UserAndGroupSelectionWidget',
                        #"Products.SimpleAttachment",
                        'eduintelligent.trainingcenter',
                        #"eduintelligent.database",
                        #"eduintelligent.loginhistory",
                        'eduintelligent.evaluation',
                        #"eduintelligent.zipcontent",
                        #"eduintelligent.sco",
                        'eduintelligent.courses',
                        #"eduintelligent.messages",
                        #"Products.Faq",
                        #"eduintelligent.paeduintelligent",  
                        #"Products.PloneSurvey",
                        #"Products.PloneArticle",
                        #"Products.PloneHelpCenter",
                        #"Products.PloneGlossary",
                        #"Products.PlonePopoll",
                        #"Products.Ploneboard",
                        #"Products.MasterSelectWidget",
                        )

EXTENSION_PROFILES = ('eduintelligent.policy:default',)

def install(self, reinstall=False):
    """Install a set of products (which themselves may either use Install.py
    or GenericSetup extension profiles for their configuration) and then
    install a set of extension profiles.
    
    One of the extension profiles we install is that of this product. This
    works because an Install.py installation script (such as this one) takes
    precedence over extension profiles for the same product in 
    portal_quickinstaller. 
    
    We do this because it is not possible to install other products during
    the execution of an extension profile (i.e. we cannot do this during
    the importVarious step for this profile).
    """
    
    portal_quickinstaller = getToolByName(self, 'portal_quickinstaller')
    portal_setup = getToolByName(self, 'portal_setup')

    for product in PRODUCT_DEPENDENCIES:
        if reinstall and portal_quickinstaller.isProductInstalled(product):
            portal_quickinstaller.reinstallProducts([product])
            transaction.savepoint()
        elif not portal_quickinstaller.isProductInstalled(product):
            portal_quickinstaller.installProduct(product)
            transaction.savepoint()
    
    for extension_id in EXTENSION_PROFILES:
        portal_setup.runAllImportStepsFromProfile('profile-%s' % extension_id, purge_old=False)
        product_name = extension_id.split(':')[0]
        portal_quickinstaller.notifyInstalled(product_name)
        transaction.savepoint()
        
