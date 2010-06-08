from Products.remember.utils import getAdderUtility
from Products.CMFCore.utils import getToolByName

from config import DEFAULT_MEMBER_TYPE

def setupNewDefaultMember(context):
    """ Setup preferred default_member_type """
    #portal = context.getSite()
    #addr = getAdderUtility(portal)
    #addr.default_member_type = DEFAULT_MEMBER_TYPE
    pass
    
def setupHideToolsFromNavigation(context):
    """hide tools"""
    # uncatalog tools
    site = context.getSite()
    toolnames = ['portal_tctool']
    portalProperties = getToolByName(context, 'portal_properties')
    navtreeProperties = getattr(portalProperties, 'navtree_properties')
    if navtreeProperties.hasProperty('idsNotToList'):
        for toolname in toolnames:
            try:
                portal[toolname].unindexObject()
            except:
                pass
            current = list(navtreeProperties.getProperty('idsNotToList'))
            if toolname not in current:
                current.append(toolname)
                kwargs = {'idsNotToList': current}
                navtreeProperties.manage_changeProperties(**kwargs)
                
def setupHideTypesFromNavigation(context):
    """hide types"""
    site = context.getSite()
    typesnames = ['eduMember','Large Plone Folder','Event','News Item','MemberDataContainer']
    portalProperties = getToolByName(context, 'portal_properties')
    navtreeProperties = getattr(portalProperties, 'navtree_properties')
    if navtreeProperties.hasProperty('metaTypesNotToList'):
        for typename in typesnames:
            current = list(navtreeProperties.getProperty('metaTypesNotToList'))
            if typename not in current:
                current.append(typename)
                kwargs = {'metaTypesNotToList': current}
                navtreeProperties.manage_changeProperties(**kwargs)