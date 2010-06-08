# -*- coding: utf-8 -*-
##
## Copyright (C) 2005-2007 Ingeniweb
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
Misc import steps for GenericSetup (see profiles/default/import-steps.xml)
$Id: ExFile.py 6229 2007-08-02 13:30:44Z glenfant $
"""
__docformat__ = 'restructuredtext'
__author__ = ''

from zope.interface import implements
from Products.CMFQuickInstallerTool.interfaces import INonInstallable
from Products.CMFEditions.StandardModifiers import manage_addOMInsideChildrensModifier
from Products.ATContentTypes.configuration import zconf as atct_zconf
from Products.PloneArticle.config import PROJECTNAME, PLONEARTICLE_TOOL
from Products.CMFCore.utils import getToolByName

class HiddenProductsNProfiles(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        return [] #[u'Products.PloneArticle:default',]

    def getNonInstallableProducts(self):
        # hides "Products.PloneArticle": only "PloneArticle"
        return ['Products.PloneArticle',]


def thisProfileOnly(func):
    """Decorator that prevents the setup func to be used on other GS profiles.
    Usage:
    @thisProfileOnly
    def someFunc(context): ...
    """

    def wrapper(context):
        if context.readDataFile('plonearticle.txt') is None:
            return
        else:
            return func(context)
    return wrapper


@thisProfileOnly
def setupTool(context):
    """ Create PloneArticleTool at site root """

    site = context.getSite()

    atool = getattr(site, PLONEARTICLE_TOOL, None)

    if atool is None:
        site.manage_addProduct[PROJECTNAME].manage_addTool('PloneArticleTool')
        atool = getattr(site, PLONEARTICLE_TOOL, None)
        atool.setVersionFromFS()

    numvers, version = atool.getVersion()
    if not numvers and not version:
        # we are reinstalling over an older version. Set to the first one from
        # which we can migrate
        atool.setInstanceVersion('3.2.99')

    return 'PloneArticleTool  created'


@thisProfileOnly
def setupModifier(context):
    """Add a modifier for PloneArticle for CMFEditions"""

    mod_id = 'PloneArticleModifier'
    portal_modifier = context.getSite().portal_modifier
    if mod_id in portal_modifier.objectIds():
        # We delete and recreate that modifier
        portal_modifier._delObject(mod_id)
    manage_addOMInsideChildrensModifier(portal_modifier, mod_id)
    modifier = getattr(portal_modifier, mod_id)
    modifier.edit(enabled=True, condition="python:meta_type == 'PloneArticle'")
    return "CMFEdition modifier for PloneArticle added"


@thisProfileOnly
def setupKupu(context):
    """Update kupu properties"""

    # Should be done by GS with kupu.xml but exportimport.py of kupu supports only full configuration

    site = context.getSite()
    ktool = getattr(site, 'kupu_library_tool', None)
    typestool = getToolByName(site, 'portal_types')
    if ktool and typestool:

        available_types = typestool.listContentTypes()
        kupu_resources = {
            'linkable': ('PloneArticle','ImageInnerContentProxy','FileInnerContentProxy'),
            'mediaobject': ('ImageInnerContentProxy',),
            'containsanchors': ('PloneArticle',),
            'collection': ('PloneArticle', 'InnerContentContainer')
            }

        for resource_type in ('linkable', 'mediaobject', 'containsanchors', 'collection'):
            new_types = list(ktool.getPortalTypesForResourceType(resource_type))
            
            # avoid bugs with ktool.getPortalTypesForResourceType
            # sometimes unavailable types can be always registered after a product uninstall
            for type_id in new_types :
                if type_id not in available_types :
                    new_types.remove(type_id)
                    print 'contenttype removed from kupu resource %s : %s \n' %(resource_type, type_id )
                    
            for type_id in kupu_resources[resource_type]:
                if type_id in new_types:
                    continue 
                new_types.append(type_id)
            new_resources = []
            new_resources.append({
                'old_type': resource_type,
                'resource_type': resource_type,
                'portal_types': new_types})
            ktool.updateResourceTypes(new_resources)
        return 'Kupu set for PloneArticle'
    else:
        return 'Kupu not installed'

DEFAULT_MAX_SIZE = 3 * 2 ** 20

@thisProfileOnly
def setupFTI(context):
    """Sets FTI max size default props as in ATCT config"""

    site = context.getSite()
    try:
        fti = site.portal_types.PloneArticle
    except AttributeError, e:
        return "PloneArticle FTI not installed in portal_types"

    fti.attachmentMaxSize = int(atct_zconf.ATFile.max_file_size) or DEFAULT_MAX_SIZE
    fti.imageMaxSize = int(atct_zconf.ATImage.max_file_size) or DEFAULT_MAX_SIZE
    return "PlonArticle FTI has ATCT defaults"
