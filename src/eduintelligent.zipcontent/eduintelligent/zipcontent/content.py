# -*- coding: utf-8 -*-
#
# File: content.py
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

#### Standard Python modules
import os
from StringIO import StringIO

#### Standard Zope modules
from zope.interface import implements
from zope.component.factory import Factory
from zope.annotation.interfaces import IAnnotations

#### Standard Products Plone
from Products.CMFCore.utils import getToolByName
from plone.locking.interfaces import ITTWLockable
from plone.app.content.interfaces import INameFromTitle
from plone.app.content.item import Item

#### 3rd Products imports

#### Local modules
from eduintelligent.zipcontent import zipcontentMessageFactory as _
from eduintelligent.zipcontent.interfaces import IZipContent
from eduintelligent.zipcontent.config import PROJECTNAME, CONTENT_STORE, EXTERNAL_URL
from eduintelligent.zipcontent import utilities

class ZipContent(Item):
    implements(IZipContent, ITTWLockable, INameFromTitle)
    portal_type = "ZipContent"
    
    title = u""
    description = u""
    filename = u""
    
    def getUrlContents(self):
        """
        """
        zipcontentId = "/".join(self.getPhysicalPath())
        return EXTERNAL_URL + zipcontentId

    def storePathZip(self):
        """
        """
        zipcontentId = "/".join(self.getPhysicalPath())
        path = os.path.join(CONTENT_STORE, zipcontentId.lstrip('/'))
        return path

    def protectDirs(self):
        """
        :> robots.txt
        User-agent: *    # aplicable a todos
        Disallow: /      # impide la indexacion de todas las paginas
        ##################################
        :> .htaccess
        chmod 644 .htaccess
        IndexIgnore *
        """
        def walker(directory):
            for name in os.listdir(directory):
                path = os.path.join(directory,name)
                if os.path.isdir(path):
                    f = open(os.path.join(path,'robots.txt'),'w')
                    f.write("""User-agent: *\nDisallow: /
                    """)
                    f.close()
                    f = open(os.path.join(path,'.htaccess'),'w')
                    f.write("""IndexIgnore *\n""")
                    f.close()
                    walker(path)
                    os.chmod(os.path.join(path,'robots.txt'), 0644)
                    os.chmod(os.path.join(path,'.htaccess'), 0644)

        zipcontentId = "/".join(self.getPhysicalPath())
        path = os.path.join(CONTENT_STORE, zipcontentId.lstrip('/'))
        walker(path)

    def uploadContentPackage(self):
        """
        this is an event after create or edit 
        """
        specificPath = self.storePathZip()
        print "Ruta en donde se almacena: ", specificPath
        if hasattr(self.filename,'data'):
            if os.path.exists(specificPath):
                # we want to replace an existing directory:
                utilities.removeDirectory(specificPath)
            
            utilities.createDirectory(specificPath)        

            utilities.unzip().extract(StringIO(str(self.filename.data)),specificPath)
            self.protectDirs()  ### create files to protect the public files

        self._v_manifest = None   # invalidate manifest after upload
        self._v_itemCount = None
        self.filename = None

    def getFileFromContentPackage(self, subpath, doStream=False):
        path = os.path.join(self.storePathZip(), subpath)
        if not os.path.exists(path):
            print "cuidado, no existe el archivo!!"
            return ''
        f = open(path)
        return f.read()

zipcontentFactory = Factory(ZipContent, title=_(u"Create a new ZipContent"))
