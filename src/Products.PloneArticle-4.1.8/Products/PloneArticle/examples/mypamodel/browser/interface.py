# -*- coding: utf-8 -*-
## Copyright (C)2007 Ingeniweb

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

class IPAViewWithAuthor(Interface):
    """
    Just a marker interface.
    """

    def authorInfo():
        """
        Provides some useful information about the author as a mapping
        with keys:
        * fullname: M. John doe
        * url: show a page about the author
        * portrait: a small image of the author
        """
