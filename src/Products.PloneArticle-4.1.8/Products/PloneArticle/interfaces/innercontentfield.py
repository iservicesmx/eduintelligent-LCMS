# -*- coding: utf-8 -*-
## Defines interfaces inherited from IBaseInnerContentField
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
Defines interfaces inherited from IBaseInnerContentField
"""

__docformat__ = 'restructuredtext'

# Zope imports
from zope.interface import Interface

class IBaseInnerContentField(Interface):
    """"""
    
    pass

class IFileInnerContentField(IBaseInnerContentField):
    """"""
    
    pass

class IImageInnerContentField(IBaseInnerContentField):
    """"""
    
    pass
    
class ILinkInnerContentField(IBaseInnerContentField):
    """"""
    
    pass

class IBaseInnerContent(Interface):
    """"""
    
    pass

class IInnerContentContainer(Interface):
    """"""
    
    pass
