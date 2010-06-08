# -*- coding: utf-8 -*-
## Defines utilities to use with article models
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
Defines utilities to use with article models
"""

__docformat__ = 'restructuredtext'

# Zope imports
from zope.interface import implements
from Products.Five import BrowserView
import modelsconfig

def _getThumbUrl(image_url, width, height) :
    """
    Return a thumb url 
    without image.getObject
    """
    return '%s/pa_thumb/imagex%ix%i.jpeg' %(image_url, width, height)
    
def _getImageInfo(image, pwidth, pheight, twidth, theight):
    """
    all informations to display a proxy image
    """   
    image_url = image.absolute_url()
    return dict( thumb_url = _getThumbUrl(image_url, twidth, theight),
                 preview_url = _getThumbUrl(image_url, pwidth, pheight),
                 image_url = image_url,
                 title = image.title_or_id(),
                 description = image.Description(), )    
    

# Products imports
from interface import IPloneArticleModelView, IPloneArticleModel1View, \
     IPloneArticleModel2View, \
     IPloneArticleModel3View, \
     IPloneArticleModel4View, \
     IPloneArticleModel5View, \
     IPloneArticleModel6View, \
     IPloneArticleModel7View, \
     IPloneArticleModel8View, \
     IPloneArticleModel9View, \
     IPloneArticleModel10View, \
     IPloneArticleModel11View

from Products.PloneArticle.interfaces import IFileInnerContentProxy, \
    IImageInnerContentProxy
from Products.PloneArticle.model import registerArticleModel

from Products.PloneArticle.i18n import ModelMessageFactory as _

class PloneArticleModelView(BrowserView):
    """
    No description available
    """
    implements(IPloneArticleModelView)

    template_id = ''
    title = u'Untitled model'
    title_mgsid = 'untitled_model'
    icon = 'pa_default_model.gif'
    description_msgid = 'no_description_available'
    
    def __init__(self, context, request):
      self.context = context
      self.request = request

    def Title(self):
        """Return the translated title of this model"""
        return _(self.title_msgid, default=self.title)
    
    def getDefaultImageSize(self):
        """Returns default dimension(width, height) of an image"""
        
        return 100, 130
        
        
    def getBigImageSize(self):
        """Returns dimension(width, height) for a big image"""
        
        return 500, 350     
           
    
    def getImageUrl(self, proxy):
        """Returns url to access image of an ImageInnerContentProxy object
        """

        if not IImageInnerContentProxy.providedBy(proxy):
            raise ValueError, "Proxy must implements IImageInnerContentProxy"
        
        return proxy.absolute_url()
    
    def getImageBlockStyle(self, proxy):
        """Returns style of block containing the img tag rendering an ImageInnerContentProxy object"""
        
        if not IImageInnerContentProxy.providedBy(proxy):
            raise ValueError, "Proxy must implements IImageInnerContentProxy"
        
        width, height = self.getDefaultImageSize()
        style = 'width: %d; height: %d;' % (width, height)
        return style
        
    def getImageTag(self, proxy):
        """Returns an img tag rendering an ImageInnerContentProxy object
        """
        
        if not IImageInnerContentProxy.providedBy(proxy):
            raise ValueError, "Proxy must implements IImageInnerContentProxy"
        
        width, height = self.getDefaultImageSize()
        params={}
        params['width']=width
        params['height']=height
        # use description as title when possible
        legend=proxy.Description()
        if legend :
          params['title']=legend
        return proxy.tag(**params)
        
    def getBigImageTag(self, proxy):
        """Returns a big img tag rendering an ImageInnerContentProxy object
        """
        
        if not IImageInnerContentProxy.providedBy(proxy):
            raise ValueError, "Proxy must implements IImageInnerContentProxy"
        
        width, height = self.getBigImageSize()
        return proxy.tag(width=width, height=height)       

    def getImageTile(self, proxy):
        """Returns a 16px icon from an ImageInnerContentProxy object
        """
        
        if not IImageInnerContentProxy.providedBy(proxy):
            raise ValueError, "Proxy must implements IImageInnerContentProxy"
        
        return proxy.tag(width=16, height=16)    
        

    def getSmallImage4Crop(self, proxy):
        """Returns at least a 50*50px img tag from an ImageInnerContentProxy object
        """
        
        if not IImageInnerContentProxy.providedBy(proxy):
            raise ValueError, "Proxy must implements IImageInnerContentProxy"
        
        params={} 
        params['maximizeTo'] = 50
        params['maxRatio'] = 1   
        legend=proxy.Title()
        if legend :
            params['title']=legend
        return proxy.tag(**params)        
        
    def getImage4Crop(self, proxy):
        """Returns at least a 250*250px img tag from an ImageInnerContentProxy object
        """
        
        if not IImageInnerContentProxy.providedBy(proxy):
            raise ValueError, "Proxy must implements IImageInnerContentProxy"
        
        params={}
        params['maximizeTo']=250
        params['maxRatio'] = 1   
        legend=proxy.Title()
        if legend :
            params['title']=legend
        return proxy.tag(**params)              

    def getFileUrl(self, proxy):
        """Returns url to access file of an FileInnerContentProxy object
        """
        
        if not IFileInnerContentProxy.providedBy(proxy):
            raise ValueError, "Proxy must implements IImageInnerContentProxy"
        
        return proxy.absolute_url()
        
        
    

class PloneArticleModel1View(PloneArticleModelView):
    """
    Images are displayed on the right, while attachments are on the bottom of
    the document.

    This is a simple layout that can be used for documentation, for example.
    """
    implements(IPloneArticleModel1View)

    template_id = 'pa_model1'
    title = u'Documentation model'
    title_msgid = 'model1_title'
    icon = 'pa_model1.gif'
    description_msgid = 'model1_description'

registerArticleModel(PloneArticleModel1View)

class PloneArticleModel2View(PloneArticleModelView):
    """
    The first image is displayed in the text header.

    Other images are displayed on the right, while attachments are on the bottom
    of the document.
    
    This is a simple layout that can be used for end-user articles, for example.
    """
    implements(IPloneArticleModel2View)    

    template_id = 'pa_model2'
    title = u'Newspaper article model'
    title_msgid = 'model2_title'
    description_msgid = 'model2_description'
    icon = 'pa_model2.gif'

    def __init__(self, context, request):
        super(PloneArticleModelView, self).__init__(context, request)
        self.images = context.getImages()

    def getFirstImage(self):
        return len(self.images) > 0 and self.images[0] or None

    def getOtherImages(self):
        return self.images[1:]
    
registerArticleModel(PloneArticleModel2View)

class PloneArticleModel3View(PloneArticleModelView):
    """
    Shrinked images are placed after the description and the text.
    """
    implements(IPloneArticleModel3View)

    template_id = 'pa_model3'
    title = u'Small images'
    title_msgid = 'model3_title'
    description_msgid = 'model3_description'
    icon = 'pa_model3.gif'
    
registerArticleModel(PloneArticleModel3View)

class PloneArticleModel4View(PloneArticleModelView):
    """
    The description and the text are displayed first.
    Big images are displayed after the text.
    """
    implements(IPloneArticleModel4View)

    template_id = 'pa_model4'
    title = u'Big images'
    title_msgid = 'model4_title'
    description_msgid = 'model4_description'
    icon = 'pa_model4.gif'
    
registerArticleModel(PloneArticleModel4View)

class PloneArticleModel5View(PloneArticleModelView):
    """
    The first two images are displayed inline first. 
    Then comes the body of the article.
    All other images that illustrate the article come after and are displayed
    inline two by two.
    """
    implements(IPloneArticleModel5View)

    template_id = 'pa_model5'
    title = u'Small images separated by text'
    title_msgid = 'model5_title'
    description_msgid = 'model5_description'
    icon = 'pa_model5.gif'

    def __init__(self, context, request):
        super(PloneArticleModelView, self).__init__(context, request)
        self.images = context.getImages()

    def getHeadingImages(self):
        return self.images[:2]

    def getBodyImages(self):
        return self.images[2:]
    
registerArticleModel(PloneArticleModel5View)

class PloneArticleModel6View(PloneArticleModel2View):
    """
    The first image is big and displayed first.
    Other images are displayed after the article text.
    """
    implements(IPloneArticleModel6View)

    template_id = 'pa_model6'
    title = u'Big images separated by text'
    title_msgid = 'model6_title'
    description_msgid = 'model6_description'
    icon = 'pa_model6.gif'

registerArticleModel(PloneArticleModel6View)

class PloneArticleModel7View(PloneArticleModel2View):
    """
    The first image is big and followed by the body of the article.
    All other images come after in shrinked size.
    """
    implements(IPloneArticleModel7View)

    template_id = 'pa_model7'
    title = u'One big image and a lot of small'
    title_msgid = 'model7_title'
    description_msgid = 'model7_description'
    icon = 'pa_model7.gif'

registerArticleModel(PloneArticleModel7View)

class PloneArticleModel8View(PloneArticleModel2View):
    """
    This model diplays first an image (in its normal size), followed by the body
    of the article.
    All other images are shrinked and come after the text.
    The attachments are displayed on the left of the article.
    """
    implements(IPloneArticleModel8View)

    template_id = 'pa_model8'
    title = u'One big image and lots of small and side attachments'
    title_msgid = 'model8_title'
    description_msgid = 'model8_description'
    icon = 'pa_model8.gif'

registerArticleModel(PloneArticleModel8View)

class PloneArticleModel9View(PloneArticleModelView):
    """
    This model diplays images icons, files and links at bottom of page
    """
    implements(IPloneArticleModel9View)

    template_id = 'pa_model9'
    title = u'images icons, files and links at page bottom'
    title_msgid = 'model9_title'
    description_msgid = 'model9_description'
    icon = 'pa_model9.gif'

registerArticleModel(PloneArticleModel9View)

class PloneArticleModel10View(PloneArticleModelView):
    """
    4 first images displayed at left and cropped in a 50*50px square
    Zoom on first image displayed cropped in a 250*250px square
    Others images displayed at page bottom as icons
    """
    implements(IPloneArticleModel10View)

    template_id = 'pa_model10'
    title = u'Square cropped images'
    title_msgid = 'model10_title'
    description_msgid = 'model10_description'
    icon = 'pa_model10.gif'

    def __init__(self, context, request):
        super(PloneArticleModelView, self).__init__(context, request)
        self.images = context.getImages()
        
    def getFirstImage(self):
        return len(self.images) > 0 and self.images[0] or None        

    def getHeadingImages(self):
        return self.images[:4]
    
registerArticleModel(PloneArticleModel10View)


class PloneArticleModel11View(PloneArticleModelView):
    """
    Ajax viewer for images
    """
    implements(IPloneArticleModel11View)

    template_id = 'pa_model11'
    title = u'Ajax slide viewer'
    title_msgid = 'model11_title'
    description_msgid = 'model11_description'
    icon = 'pa_model11.gif'

    def __init__(self, context, request):
        super(PloneArticleModelView, self).__init__(context, request)
        self.images = context.getImages()
        self.maxwidth = modelsconfig.MAXWIDTH
        self.maxheight = modelsconfig.MAXHEIGHT    
        self.thumbmaxwidth = modelsconfig.THUMBMAXWIDTH
        self.thumbmaxheight = modelsconfig.THUMBMAXHEIGHT     
        self.disablestyles = modelsconfig.DISABLESTYLES   
        self.float = modelsconfig.FLOAT      
        self.bgcolor = modelsconfig.BGCOLOR      
        self.bordercolor = modelsconfig.BORDERCOLOR 
        self.margin = modelsconfig.MARGIN        
        self.controlsorientation = modelsconfig.CONTROLSORIENTATION    
        self.verticalcontrolsposition = modelsconfig.VERTICALCONTROLSPOSITION 
        self.horizontalcontrolsposition = modelsconfig.HORIZONTALCONTROLSPOSITION   


    def getPlayerImages(self):
        """
        tags & image's urls for player
        """      
        images = []
        all_views = self.images
        for image in all_views :
            imageInfo = _getImageInfo (image, self.maxwidth, self.maxheight,
                                       self.thumbmaxwidth, self.thumbmaxheight)
            images.append(imageInfo)
                               
        return len(all_views) > 0 and images or None
        

        
    def _getGlobalStyle(self):
        """
        Player global style
        Return only width if global styles disabled
        """              
        if self.disablestyles :
            return 'width: %ipx' %self.maxwidth
        return '''width: %ipx; 
                  clear: %s;
                  float: %s;
                  margin: %s;
                  border-color:%s;
                  background-color: %s''' %(self.maxwidth, self.float, self.float, self.margin,
                                            self.bordercolor, self.bgcolor ) 
                                            
    def _getGlobalClass(self):
        """
        Player global class (vertical or horizontal, vertical buttons on left or right)
        """              
        
        return '%sPlayer %sVButtons %sHButtons' %(self.controlsorientation, self.verticalcontrolsposition,
                                                  self.horizontalcontrolsposition )                                                
        
    def getPlayerStyle(self):
        """
        Player width & height & global style
        """      
        
        return {'maxwidth' : self.maxwidth,
                'maxheight' : self.maxheight,
                'thumbmaxwidth' : self.thumbmaxwidth,
                'thumbmaxheight' : self.thumbmaxheight,  
                'globalstyles': self._getGlobalStyle(),  
                'globalclass': self._getGlobalClass(),}
                
    def getPlayerFirstImage(self):
        """
        tags & image's urls for first image player
        displayed even when javascript is disabled
        """                      
        images = self.images
        return len(images) > 0 and _getImageInfo (images[0], self.maxwidth, self.maxheight,
                                       self.thumbmaxwidth, self.thumbmaxheight) or None

    
registerArticleModel(PloneArticleModel11View)
