# -*- coding: utf-8 -*-
## This module contains all content types used in PloneArticle product
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
This module contains all content types used in PloneArticle product
"""

__docformat__ = 'restructuredtext'

# Inner content interfaces
from innercontentproxy import IBaseInnerContentProxy, IFileInnerContentProxy, \
    IImageInnerContentProxy, ILinkInnerContentProxy

from innercontentfield import IBaseInnerContentField, IFileInnerContentField, \
    IImageInnerContentField, ILinkInnerContentField, IBaseInnerContent, \
    IInnerContentContainer

from innercontentwidget import IBaseInnerContentWidget, \
    IFileInnerContentWidget, IImageInnerContentWidget, ILinkInnerContentWidget

from article import IPloneArticle, IPloneArticleMultiPage, IPloneArticleTool

from smartlistfield import ISmartListField

# We need this as long as we will support both Plone 2.1 & 2.5 : 2.1 does not
# provide a Z3 interface for INonStructuralFolder, but Plone 2.5 require that it
# is implemented with a Z3 one to take it into account (see implement.zcml)
try:
    from Products.CMFPlone.interfaces.structure import INonStructuralFolder
except ImportError:
    from Products.CMFPlone.interfaces.NonStructuralFolder import \
         INonStructuralFolder as z2_INonStructuralFolder
    from Products.Five.bridge import fromZ2Interface
    INonStructuralFolder = fromZ2Interface(z2_INonStructuralFolder)
