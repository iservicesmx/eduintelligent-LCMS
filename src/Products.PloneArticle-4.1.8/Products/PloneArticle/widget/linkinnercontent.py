# -*- coding: utf-8 -*-
## Defines LinkInnerContentWidget
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
Defines LinkInnerContentWidget
"""

__docformat__ = 'restructuredtext'

# Zope imports
from AccessControl import ClassSecurityInfo

# Archetypes imports
from Products.Archetypes.Registry import registerWidget

# Products imports
from Products.PloneArticle.widget import BaseInnerContentWidget

class LinkInnerContentWidget(BaseInnerContentWidget):
    """"""
    
    _properties = BaseInnerContentWidget._properties.copy()
    _properties.update({
        'macro' : "pa_linkinnercontentwidget",
        })

    security = ClassSecurityInfo()
    
registerWidget(LinkInnerContentWidget,
               title='LinkInnerContent',
               description=(''),
               used_for=('Products.PloneArticle.field.linkinnercontent.LinkInnerContentField',)
               )
