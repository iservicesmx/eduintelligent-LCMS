# -*- coding: utf-8 -*-
## PloneArticle product provides content with files, images, links
## Copyright (C)2006 Ingeniweb

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
This module contains utilities, helpers
"""

from Products.CMFCore.utils import getToolByName
from Products.PloneArticle.interfaces import \
     IBaseInnerContentProxy as z2_IBaseInnerContentProxy


def find_classes_implementing_method(klass, method_name):
    """Returns a list of classes implementing a given method.

    @param method_name: Name of the method we are searching for
    """

    if method_name in klass.__dict__.keys():
        return (klass,)

    base_klasses = klass.__bases__
    result = []
    for base_klass in base_klasses:
        result.extend(find_classes_implementing_method(base_klass, method_name))

    return tuple(result)

def getAllAvailableReferenceableTypes(context, klass):
    ## XXX perhaps check that klass is an instance of something correct ?
    interfaces = klass.getReferenceableInterfaces()

    at = getToolByName(context, 'archetype_tool')
    proxy_types = at.listPortalTypesWithInterfaces([z2_IBaseInnerContentProxy,])
    proxy_types = [fti.getId() for fti in proxy_types]

    ## ct are content types implemented by these interfaces but
    ## which are not proxies
    ct = at.listPortalTypesWithInterfaces(interfaces)
    ct = [c_fti.getId() for c_fti in ct]
    ct = [pt for pt in ct if not pt in proxy_types]
    return ct


