# -*- coding: utf-8 -*-
## Declare PloneArticle interface
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
Declare PloneArticle interface
"""

__docformat__ = 'restructuredtext'

from zope.interface import Interface

# Products imports
from Products.ATContentTypes.interface import IATDocument

# This is a marker interface. By having PloneArticle declare that it implements
# IPloneArticle, we are asserting that it also supports IATDocument and
# everything that interface declares

class IPloneArticle(IATDocument):
    """PloneArticle marker interface"""
    pass

class IPloneArticleMultiPage(Interface):
    """MultiPage interface"""

    def getPages(self):
        """
        Return the ordered list of articles
        """

class IPloneArticleTool(Interface):
    """Services and options for PloneArticle contents"""
    pass
