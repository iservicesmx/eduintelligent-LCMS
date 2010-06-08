# -*- coding: utf-8 -*-
## Defines ImageInnerContentField
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
Defines ImageInnerContentProxy
"""

__docformat__ = 'restructuredtext'

# Zope imports
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from OFS.Image import Image

# CMF imports
from Products.CMFCore import permissions as CCP
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.public import ImageField, ImageWidget, ReferenceField, \
    registerType, Schema, ComputedField, ComputedWidget

# Products imports
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget

from Products.ATContentTypes.interface import IImageContent

from Products.PloneArticle import LOG
from Products.PloneArticle.proxy import BaseFileContentProxy, \
    BaseInnerContentProxySchema
from Products.PloneArticle.interfaces import IImageInnerContentProxy, IBaseInnerContentProxy
from Products.PloneArticle.config import PLONEARTICLE_TOOL


# Defines schema
ImageInnerContentProxySchema = BaseInnerContentProxySchema.copy() + Schema((
    ComputedField(
        'image',
        primary=True,
        expression="""context.getPrimaryValue('image', 'attachedImage', '')""",
        widget=ComputedWidget(
            label='Image',
            label_msgid='label_image',
            i18n_domain='plonearticle',
            ),
        ),
    ReferenceField(
        'referencedContent',
        relationship='article_image',
        keepReferencesOnCopy=True,
        widget=ReferenceBrowserWidget(
            label='Referenced image',
            label_msgid='label_referenced_image',
            i18n_domain='plonearticle',
            ),
        ),
    ImageField(
        'attachedImage',
        attached_content=True,
        widget=ImageWidget(
            label='Attached image',
            label_msgid='label_attached_image',
            i18n_domain='plonearticle',
            ),
        ),
    ))
    
ImageInnerContentProxySchema['title'].required = False

class ImageInnerContentProxy(BaseFileContentProxy):
    """Proxy implementing IImageContent. It means this proxy has a getImage 
    method.
    
    getImage returns attached image by default if existing otherwise returns
    the referenced content.
    """
    
    security = ClassSecurityInfo()
    implements(IImageInnerContentProxy)
    
    schema = ImageInnerContentProxySchema

    # You can only reference content implementing IImageContent interface
    referenceable_interfaces = (IImageContent,)
    
    security.declareProtected(CCP.View, 'index_html')
    def index_html(self, REQUEST=None, RESPONSE=None):
        """Make it directly viewable when entering the objects URL.
        
        We have to reproduce it to keep the same behaviour as usual for images.
        """
        
        if REQUEST is None:
            REQUEST = self.REQUEST
        if RESPONSE is None:
            RESPONSE = REQUEST.RESPONSE
        
        field = self.getPrimaryField()
        accessor = field.getAccessor(self)
        data = accessor()
        
        if not isinstance(data, Image):
            return ''
        
        return data.index_html(REQUEST, RESPONSE)
    
    security.declareProtected(CCP.View, 'tag')
    def tag(self, **kwargs):
        """Use proxy title for img tags: title and alt"""
        
        # Scale image
        patool = getToolByName(self, PLONEARTICLE_TOOL)
        return patool.getThumbnailTag(self, 'image', **kwargs)
    

    def setAttachedImage(self, value, **kwargs):
        """
        Rename proxy according to file name
        """
        field = self.getField('attachedImage')
        field.set(self, value, **kwargs)
        self.renameFromFileName(field)

registerType(ImageInnerContentProxy)
