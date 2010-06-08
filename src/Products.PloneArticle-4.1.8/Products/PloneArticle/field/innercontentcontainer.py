# -*- coding: utf-8 -*-
## Defines container of all proxy objects
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
Defines container of all proxy objects
$Id: innercontentcontainer.py 6977 2007-12-28 11:45:13Z b_mathieu $
"""

__docformat__ = 'restructuredtext'

# Zope imports
from AccessControl import ClassSecurityInfo
from zope.interface import implements

# CMF imports
from Products.CMFCore import permissions as CCP
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.OrderedBaseFolder import OrderedContainer
from Products.Archetypes.public import BaseFolderMixin, registerType, listTypes
from Products.Archetypes.interfaces import IOrderedContainer

# Other imports
from Products.PloneArticle.interfaces import IInnerContentContainer, IBaseInnerContent
from Products.PloneArticle.pafti import DynamicAllowedContentFTI

class InnerContentContainer(OrderedContainer, BaseFolderMixin):
    """This folder is a container of inner content objects"""

    implements(IInnerContentContainer, IOrderedContainer)

    _at_fti_meta_type = DynamicAllowedContentFTI.meta_type

    meta_type = 'InnerContentContainer'
    portal_type = 'InnerContentContainer'
    global_allow = False
    filter_content_types = False
    allowed_content_types = ()
    security = ClassSecurityInfo()

    # from OrderedBaseFolder.OrderedBaseFolder:
    #
    # this ensure a proper call of manage_renameObject, since OrderedContainer
    # is the first parent class
    manage_renameObject = BaseFolderMixin.manage_renameObject
##     security.declareProtected(CCP.ModifyPortalContent, 'manage_renameObject')
##     def manage_renameObject(self, id, new_id, REQUEST=None):
##         """ rename the object """
##         ptool = getToolByName(self, 'plone_utils')
##         new_id = ptool.normalizeString(new_id)
##         objidx = self.getObjectPosition(id)
##         result = BaseFolderMixin.manage_renameObject(self, id, new_id, REQUEST)
##         self.moveObject(new_id, objidx)

##         return result

    security.declareProtected(CCP.AddPortalContent, 'invokeFactory')
    def invokeFactory(self, type_name, id, RESPONSE=None, *args, **kw):
        """Add new inner content"""

        # Check if content of specified portal type implements IBaseInnerContent
        atool = getToolByName(self, 'archetype_tool')
        types = [x for x in atool.listRegisteredTypes() if x['portal_type'] == type_name]
        if not types or types and not atool.typeImplementsInterfaces(types[0], (IBaseInnerContent,)):
            raise ValueError, 'Disallowed subobject type: %s' % type_name

        # Add inner content
        ttool = getToolByName(self, 'portal_types')
        args = (type_name, self, id, RESPONSE) + args
        new_id = ttool.constructContent(*args, **kw)
        if new_id is None or new_id == '':
            new_id = id
        return new_id

    security.declarePrivate('getCMFObjectsSubsetIds')
    def getCMFObjectsSubsetIds(self, objs):
        """Overriding OrderedContainer. See IOrderedContainer.
        This overrides a bug in OrderedContainer that prevents reordering
        with moveObjectsByDelta(...)"""

        ttool = getToolByName(self, 'portal_types')
        cmf_meta_types = ttool.listContentTypes(by_metatype=1)
        cmf_types = ttool.listContentTypes()
        arch_meta_types = [t['meta_type'] for t in listTypes()]
        types = cmf_types + arch_meta_types
        ids = [obj['id'] for obj in objs if obj['meta_type'] in types]
        return ids


registerType(InnerContentContainer)
