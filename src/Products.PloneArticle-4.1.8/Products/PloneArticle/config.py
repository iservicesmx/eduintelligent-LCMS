# -*- coding: utf-8 -*-
## This module contains all configuration constants of PloneArticle product
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
This module contains all configuration constants of PloneArticle product
"""

__docformat__ = 'restructuredtext'

PROJECTNAME = 'PloneArticle'
GLOBALS = globals()
PLONEARTICLE_TOOL = 'plonearticle_tool'

## if true, example types based on PloneArticle will also be loaded
INSTALL_EXAMPLES = False

# Check for Plone 2.5 or above
# FIXME: Remove this and dependant stuffs
PLONE_2_5 = True
try:
    from Products.CMFPlone.migrations import v2_5
except ImportError:
    PLONE_2_5 = False
