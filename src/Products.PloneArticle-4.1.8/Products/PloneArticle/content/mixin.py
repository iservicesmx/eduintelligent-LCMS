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
This module contains all mixins used in PloneArticle
"""

# Zope imports
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

# CMF imports
from Products.CMFCore import permissions as CCP

# Archetypes imports
try:
    from Products.LinguaPlone.public import BaseFolder
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import BaseFolder


class ArticleMixin(BaseFolder):
    """Inherits from this mixin to get some article features"""

    security = ClassSecurityInfo()

    security.declareProtected(CCP.View, 'getArticleObject')
    def getArticleObject(self,):
        """Returns the article object itself.

        It is used by objects implementing IBaseInnerContentProxy.
        """

        return self

InitializeClass(ArticleMixin)
