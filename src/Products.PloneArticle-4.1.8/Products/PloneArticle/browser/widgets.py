## -*- coding: utf-8 -*-
## Copyright (C) 2008 Ingeniweb

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

# $Id$

# KSS Server action to edit proxies : No more used

from zope.interface import implements

from kss.core import KSSView, kssaction

from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

class PAKssEdit(KSSView):
    
    model_wrapper = ZopeTwoPageTemplateFile('templates/model_wrapper.pt')
    
    @kssaction
    def replaceModelContent (self, modelname):
        """  Used to replace all content after inline editing  """        
           
        content = self.model_wrapper(pamacro = 'here/%s/macros/main' %modelname ,
                                     context = self.context)
        core = self.getCommandSet('core')
        core.replaceInnerHTML('#pacontent', content)
