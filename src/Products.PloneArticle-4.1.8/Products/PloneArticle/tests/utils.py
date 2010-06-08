# -*- coding: utf-8 -*-
## Tools to use in test cases
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
Tools to use in test cases
"""

__docformat__ = 'restructuredtext'

# Python imports
import os

def openTestFile(name):
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, 'input', name)
    fd = open(path, 'rb')
    return fd

def loadFile(name, size=0):
    """Load file from testing directory
    """
    fd = openTestFile(name)
    data = fd.read()
    fd.close()
    return data
