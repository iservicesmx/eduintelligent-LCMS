import transaction
from Products.CMFCore.utils import getToolByName

PRODUCT_DEPENDENCIES = ()
                        
EXTENSION_PROFILES = ('eduintelligent.trainingcenter:default',)

# Install methods
def setPermissions(self):
    """
    setPermissions(self, out) => Set standard permissions / roles
    """
    # Agregando los roles
    portal = getToolByName(self, 'portal_url').getPortalObject()
    if not "Student" in portal.userdefined_roles():
        portal._addRole("Student")
        #out.write("Agregado el Rol de 'Student' al portal\n")
    if not "Instructor" in portal.userdefined_roles():
        portal._addRole("Instructor")
        #out.write("Agregado el Rol de 'Instructor' al portal\n")
    if not "Administrator" in portal.userdefined_roles():
        portal._addRole("Administrator")
        #out.write("Agregado el Rol de 'Administrator' al portal\n")
    #if not "User" in portal.userdefined_roles():
    #    portal._addRole("User")
    #    out.write("Agregado el Rol de 'Director' al portal\n")

    #out.write("Reseteando los permisos por default\n")

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
    
    #setPermissions(self)

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

    
    