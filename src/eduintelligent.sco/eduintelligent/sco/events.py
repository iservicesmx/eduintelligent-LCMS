# -*- coding: utf-8 -*-
#
# File: eduCourses/events.py
#
# Copyright (c) 2007 Erik Rivera Morales <erik@ro75.com>
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

"""
$Id$
"""

__author__ = """Erik Rivera Morales <erik@ro75.com>"""
__docformat__ = 'plaintext'
__licence__ = 'GPL'

from Acquisition import aq_base

from eduintelligent.sco.interfaces import ISCO


def uploadContentPackage(obj, event):
    """
    """
    print "DESEMPAQUETANDO %s on %s" % (obj.getPhysicalPath(), event)
    ISCO(obj).uploadContentPackage()
    
