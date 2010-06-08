# -*- coding: utf-8 -*-
## Product description
## 
## Copyright (C) 2006 Ingeniweb

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
Model management views
"""

__docformat__ = 'restructuredtext'

# Zope imports
from zope.interface import implements
from Products.Five import BrowserView

# CMF
from Products.CMFCore.utils import getToolByName

# Products imports
from interface import IPloneArticleSelectModelView
from Products.PloneArticle.model import getModelRegistry

from Products.PloneArticle.i18n import ModelMessageFactory as _

class SelectModelView(BrowserView):
    implements(IPloneArticleSelectModelView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getSelectableModels(self):
        model_ids = self.context.getAvailableLayouts()
        registry = getModelRegistry()
        result = []
        for model_id, utitle in model_ids:
            model = registry.get(model_id, None)
            if model is None:
                continue
            description = _(model.description_msgid, default=model.description)
            result.append({
                'id': model.id,
                'title': model.Title(),
                'description': description,
                'icon': model.icon,
                })
        return result
   
