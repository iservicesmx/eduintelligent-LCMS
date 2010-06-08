# -*- coding: utf-8 -*-
## Used to install PloneArticle content
## Copyright (C)2005 Ingeniweb

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING. If not, write to the
## Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
This module is used by portal_quickinstaller to install product
"""

__docformat__ = 'restructuredtext'

# Python imports
from StringIO import StringIO

# CMF
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions as CCP

# Archetypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.Archetypes.public import listTypes

# Products import
from Products.PloneArticle.config import PROJECTNAME, GLOBALS, PLONEARTICLE_TOOL


# Configlets
plonearticle_management_configlet = {
    'id': 'plonearticle_management',
    'appId': PROJECTNAME,
    'name': 'PloneArticle preferences',
    'action': 'string:$portal_url/plonearticle_tool',
    'category': 'Products',
    'permission': (CCP.ManagePortal,),
    'imageUrl': 'plonearticle_tool.gif',
    }
    
types_to_hide = (
    'FileInnerContentProxy',
    'ImageInnerContentProxy',
    'LinkInnerContentProxy',
    'InnerContentContainer',
    'PloneArticleTool',)
    
kupu_resources = {
        'linkable': ('FileInnerContentProxy',),
        'mediaobject': ('ImageInnerContentProxy',),
        'collection': ('PloneArticle', 'InnerContentContainer',)
    }

# Installation is now done via GenericSetup

# def install(self):
#     """Install PloneArticle product"""
    
#     out = StringIO()

#     # Install types
#     typeInfo = listTypes(PROJECTNAME)
#     installTypes(self, out,
#                  typeInfo,
#                  PROJECTNAME)

#     # Install skin
#     install_subskin(self, out, GLOBALS)

#     # inner content setup

#     # no wf chain
#     pw = getToolByName(self, 'portal_workflow')
#     pw.setChainForPortalTypes(types_to_hide, '')
    
#     # Update portal properties
#     ptool = getToolByName(self, 'portal_properties')
    
#     # Update site_properties.types_not_searched property
#     sprops = ptool.site_properties
#     new_types = list(sprops.types_not_searched)
#     for type_id in types_to_hide:
#         if type_id in new_types:
#             continue
#         new_types.append(type_id)
#     sprops.types_not_searched = new_types
    
#     # Update site_properties.metaTypesNotToList property
#     nprops = ptool.navtree_properties
#     new_types = list(nprops.metaTypesNotToList)
#     for type_id in types_to_hide:
#         if type_id in new_types:
#             continue
#         new_types.append(type_id)
#     nprops.metaTypesNotToList = new_types

#     # don't catalog the tool
#     atool = getToolByName(self, 'archetype_tool')
#     atool.setCatalogsByType('PloneArticleTool', ())
    
#     # Update kupu properties
#     ktool = getToolByName(self, 'kupu_library_tool')
#     for resource_type in ('linkable', 'mediaobject', 'collection'):
#         new_types = list(ktool.getPortalTypesForResourceType(resource_type))
#         for type_id in kupu_resources[resource_type]:
#             if type_id in new_types:
#                 continue
#             new_types.append(type_id)
#         new_resources = []
#         new_resources.append({
#             'old_type': resource_type, 
#             'resource_type': resource_type, 
#             'portal_types': new_types})    
#         ktool.updateResourceTypes(new_resources)
    
#     # Install tool
#     atool = getattr(self, PLONEARTICLE_TOOL, None)
#     if atool is None:
#         self.manage_addProduct[PROJECTNAME].manage_addTool('PloneArticleTool')
#         atool = getattr(self, PLONEARTICLE_TOOL, None)
#         atool.setVersionFromFS()

#     numvers, version = atool.getVersion()
#     if not numvers and not version:
#         # we are reinstalling over an older version. Set to the first one from
#         # which we can migrate
#         atool.setInstanceVersion('3.2.99')
        
#     # Install configlet
#     cptool = getToolByName(self, 'portal_controlpanel')
#     try:
#         cptool.registerConfiglet(**plonearticle_management_configlet)
#     except:
#         pass
        
#     # Add portal types to portal factory
#     ftool = getToolByName(self, 'portal_factory')
#     types_to_add = (
#         'PloneArticle', 
#         'FileInnerContentProxy', 
#         'ImageInnerContentProxy',
#         'LinkInnerContentProxy',)
#     ftypes = ftool.getFactoryTypes()
#     ftypes.update(dict([(x, 1) for x in types_to_add]))
#     ftool.manage_setPortalFactoryTypes(listOfTypeIds=ftypes.keys())
#     out.write("Types configured to use portal_factory\n")
    
#     out.write('Installation completed.\n')
#     return out.getvalue()

def uninstall(self):
    """Uninstall PloneArticle product"""
    
    out = StringIO()
    
    # Update portal properties
    ptool = getToolByName(self, 'portal_properties')
    
    # Update site_properties.types_not_searched property
    sprops = ptool.site_properties
    new_types = [x for x in sprops.types_not_searched if x not in types_to_hide]
    sprops.types_not_searched = new_types
    
    # Update site_properties.metaTypesNotToList property
    nprops = ptool.navtree_properties
    new_types = [x for x in nprops.metaTypesNotToList if x not in types_to_hide]
    nprops.metaTypesNotToList = new_types
    
    # Update kupu properties
    ktool = getToolByName(self, 'kupu_library_tool')
    typestool = getToolByName(self, 'portal_types')
    
    availables_types = typestool.listContentTypes()
    
    for resource_type in ('linkable', 'mediaobject', 'collection'):
        new_types = [x for x in ktool.getPortalTypesForResourceType(resource_type) if x in availables_types and  x not in kupu_resources[resource_type]]
        new_resources = []
        new_resources.append({
            'old_type': resource_type, 
            'resource_type': resource_type, 
            'portal_types': new_types})    
        ktool.updateResourceTypes(new_resources)
    
    # Uninstall configlets
    try:
        cptool = getToolByName(self, 'portal_controlpanel')
        cptool.unregisterApplication(PROJECTNAME)
    except:
        pass
    
    out.write('Uninstallation completed.\n')
    return out.getvalue()
