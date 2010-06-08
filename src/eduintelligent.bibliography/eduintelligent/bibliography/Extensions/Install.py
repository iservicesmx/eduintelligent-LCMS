# -*- coding: utf-8 -*-
#
# File: Install.py
#
# Copyright (c) 2007 by ['Juan Ramon Lopez Beristain']
# Generator: ArchGenXML Version 2.0-alpha svn/development
#            http://plone.org/products/archgenxml
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

__author__ = """Juan Ramon Lopez Beristain <ramon@ro75.com>"""
__docformat__ = 'plaintext'


from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.eduBiblio.config import PROJECTNAME
import transaction

EXTENSION_PROFILES = ('eduintelligent.bibliography:default',)

def install(self, reinstall=False):
    """External Method to install eduBiblio
    
    This method to install a product is kept, until something better will get
    part of Plones front end, which utilize portal_setup.
    """

    portal_quickinstaller = getToolByName(self, 'portal_quickinstaller')
    portal_setup = getToolByName(self, 'portal_setup')
    
    
    for extension_id in EXTENSION_PROFILES:
        portal_setup.runAllImportStepsFromProfile('profile-%s' % extension_id, purge_old=False)
        product_name = extension_id.split(':')[0]
        portal_quickinstaller.notifyInstalled(product_name)
        transaction.savepoint()

