# -*- coding: utf-8 -*-
## Product description
## 
## Copyright (C) 2006 Ingeniweb

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
Explorer view
"""

__docformat__ = 'restructuredtext'

# Zope imports
import zLOG
from zope.interface import Interface, implements
from Products.Five import BrowserView

from Products.CMFCore.utils import getToolByName

from Products.ATContentTypes.interface import IImageContent

from interface import IExplorerView
from Products.PloneArticle.config import PLONEARTICLE_TOOL as TOOL_ID
from Products.PloneArticle.interfaces import IPloneArticle

class ExplorerView(BrowserView):
    """View for article explorer
    """
    implements(IExplorerView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

        self.path = {'query': '/'.join(context.getPhysicalPath()) }
        self.article = request.get('current_article', None)
        if self.article is None:
            raise ValueError, ("%s called without 'current_article' in REQUEST",
                               self.__class__.__name__)
        
        self.field_name = request.get('field_name', None)
        self.scope = request.get('scope', '')
        self.searchTerm = request.get('searchTerm', None)
        if self.field_name is None:
            raise ValueError, (
                "Invalid: %s called without 'field_name' in request"
                % self.__class__.__name__)

        # a proper call is self.queryMethod.aq_inner: if you don't do that,
        # getFolderContents will issue an AttributeError for
        # 'portal_membership', for instance        
        if context.portal_type == 'Topic' or self.searchTerm :
            self.queryMethod = [context.queryCatalog]
            if self.scope=='portal':
               self.path={}
        else:
            self.queryMethod = [context.getFolderContents] 
            self.path['depth']=1
        self.isArticle = IPloneArticle.providedBy(context)

    def getFolders(self):
        if self.isArticle:
            return []
        if self.searchTerm:
            return []    
        return self.queryMethod[0]({'path': self.path,
                                    'is_folderish': True})
    
    def getReferenceableContent(self):
        pa_tool = getToolByName(self.context, TOOL_ID)
        field = self.article.getField(self.field_name)        
        proxy = field.getTemporaryInnerContent(self.article)
        ref_types = proxy.getReferenceablePortalTypes(field)
        results = self.queryMethod[0]({'path': self.path,
                                       'portal_type': ref_types,
                                       'SearchableText': self.searchTerm })
        return results

    def isImage(self, obj):
        return IImageContent.providedBy(obj)


    def getOrientationFor(self, image_obj):        

        field = image_obj.getField('image')
        im_width, im_height = field.getSize(image_obj)
        height = width = 0

        if im_height >= im_width:
            return 'portrait'

        return 'landscape'
                                       
    #FIXME: return an HTML tag is sooooo ugly
    def getThumbNailTagFor(self, image_obj):
        
        title = image_obj.title_or_id()
        pa_tool = getToolByName(self.context, TOOL_ID)

        # compute thumbnail
        field = image_obj.getField('image')
        im_width, im_height = field.getSize(image_obj)
        tag_size = 0

        if im_height >= im_width:
            tag_size = 100
        else:
            tag_size = int(70 * im_width / im_height)    
            
        return pa_tool.getThumbnailTag(image_obj, 'image',
                                       maximizeTo=tag_size,
                                       title='Select %s' % title,
                                       alt='Select %s' % title)                                       
