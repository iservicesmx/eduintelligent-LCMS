# -*- coding: utf-8 -*-
## This module contains all article model inerfaces
## Copyright (C)2006 Ingeniweb

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
This module contains all article model interfaces
"""

__docformat__ = 'restructuredtext'

# Zope imports
from zope.interface import Interface, Attribute
from plone.app.layout.navigation.interfaces import IDefaultPage

class IPloneArticleMultipageView(Interface):
    """View for articles containers"""

    def isMultipage(self):
        """True if in a multipage context"""

    def getPages(self):
        """Return pages as catalog brains"""

    def getTOCItems(self, context=None):
        """return a structure for display the TOC menu"""

    def getPreviousPage(self, context):
        """Catalog brain of the previous page of context"""

    def getNextPage(self, context):
        """Catalog brain of the next page of context"""

class IExplorerView(Interface):
    """View for explorer (for referencing content in articles)

    The request should have 'current_article', 'field_name' parameters
    """

    def getFolders(self):
        """Return a list of folders brain in context
        """

    def getReferenceableContent(self):
        """Return a list of brains for content that are referenceable for the
        current field"""

    def isImage(self, obj):
        """obj implements IImageContent"""

    def getThumbNailTagFor(self, image):
        """Return a proper img thumbnail tag for given image object"""

    def getOrientationFor(self, image):
        """Return orientation class for given image object"""
        
class IPloneArticleSelectModelView(Interface):
    """View for the 'select model' page"""

    def getSelectableModels(self):
        """return a list of dict with id, title, description and icon values"""

class IPloneArticleModelView(Interface):
    """View for all article models"""

    template_id = Attribute('template_id',
                            'Must be set to a unique template name')

    title = Attribute('title',
                      'The user friendly title of this model')
    
    def getImageUrl(proxy):
        """Returns url to access image of an ImageInnerContentProxy object"""
    
    def getImageTag(proxy):
        """Returns an img tag rendering an ImageInnerContentProxy object"""
    
    def getImageTile(proxy):
        """Returns a 16px icon from an ImageInnerContentProxy object"""
    
    def getBigImageTag(proxy):
        """Returns a big img tag rendering an ImageInnerContentProxy object"""
    
    def getImage4Crop(proxy):
        """Returns a 250px img tag from an ImageInnerContentProxy object"""
    
    def getSmallImage4Crop(proxy):
        """Returns a 50px img tag from an ImageInnerContentProxy object"""
        
    def getImageBlockStyle(proxy):
        """Returns style of block containing the img tag rendering an ImageInnerContentProxy object"""
    
    def getFileUrl(proxy):
        """Returns url to access file of an FileInnerContentProxy object"""
        
    
class IPloneArticleModel1View(Interface):
    """View for article model 1"""
    
class IPloneArticleModel2View(Interface):
    """View for article model 2"""

    def getFirstImage(self):
        pass

    def getOtherImages(self):
        pass
    
class IPloneArticleModel3View(Interface):
    """View for article model 3"""

class IPloneArticleModel4View(Interface):
    """View for article model 4"""

class IPloneArticleModel5View(Interface):
    """View for article model 5"""

    def getHeadingImages(self):
        pass

    def getBodyImages(self):
        pass

class IPloneArticleModel6View(Interface):
    """View for article model 6"""

    def getFirstImage(self):
        pass

    def getOtherImages(self):
        pass

class IPloneArticleModel7View(Interface):
    """View for article model 7"""

    def getFirstImage(self):
        pass

    def getOtherImages(self):
        pass

class IPloneArticleModel8View(Interface):
    """View for article model 8"""

    def getFirstImage(self):
        pass

    def getOtherImages(self):
        pass

class IPloneArticleModel9View(Interface):
    """View for article model 9"""        
    
    
class IPloneArticleModel10View(Interface):
    """View for article model 10"""

    def getFirstImage(self):
        pass

    def getHeadingImages(self):
        pass
        
class IPloneArticleModel11View(Interface):
    """View for article model 11"""


    def getPlayerImages(self):
        pass

    def getPlayerStyle(self):
        pass    

    def getPlayerFirstImage(self):
        pass    
