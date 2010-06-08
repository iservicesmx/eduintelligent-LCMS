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

from Products.Archetypes.Registry import Registry, getDoc
from Products.PloneArticle.browser.interface import IPloneArticleModelView

from Products.PloneArticle.i18n import ModelMessageFactory as _

class ModelDescription:

    __allow_access_to_unprotected_subobjects__ = 1

    def __init__(self, klass, title='', description=''):
        if not IPloneArticleModelView.implementedBy(klass):
            raise ValueError, \
                  "%s does not implement IPloneArticleModelView" % repr(klass)
        
        self.id = klass.template_id
        self.klass = klass
        self.title = title or klass.title or klass.__name__
        self.title_msgid = klass.title_msgid
        self.description = description or getDoc(klass)
        self.description_msgid = klass.description_msgid
        self.icon = klass.icon
        
    def Title(self):
        """Return the translated title of this model"""
        return _(self.title_msgid, default=self.title)

    def Description(self):
        """Return the translated description"""
        return _(self.description_msgid, default=self.description)

modelRegistry = Registry(ModelDescription)

def registerArticleModel(klass):
    """
    """
    model = ModelDescription(klass)
    modelRegistry.register(model.id, model)

def getModelRegistry():
    return modelRegistry
