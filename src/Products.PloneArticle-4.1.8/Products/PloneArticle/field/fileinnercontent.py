# -*- coding: utf-8 -*-
## Defines FileInnerContentField
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
Defines FileInnerContentField
"""

__docformat__ = 'restructuredtext'

# Zope imports
from AccessControl import ClassSecurityInfo
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.Registry import registerField

# Products imports
from Products.PloneArticle.field import BaseInnerContentField
from Products.PloneArticle.interfaces import IFileInnerContentField

class FileInnerContentField(BaseInnerContentField):
    """Defines proxy managing files"""
 
    implements(IFileInnerContentField)
    _properties = BaseInnerContentField._properties.copy()
    _properties.update({
        'inner_portal_type' : 'FileInnerContentProxy',
        })

    security = ClassSecurityInfo()

registerField(FileInnerContentField,
              title='FileInnerContent',
              description=('Used to store FileInnerContentProxy objects.')
             )
