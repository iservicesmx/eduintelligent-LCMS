# -*- coding: utf-8 -*-
## Copyright (C)2008 Erik Rivera Morales

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
The interfaces for our models
$Id$
"""

# Zope imports
from zope.interface import Interface, Attribute

class IPAEduIntelligent(Interface):
    """View for article model 0"""
    def transform(text):
        """transform edutags to html"""
        pass
        
    def getPages():
        """split the text"""
