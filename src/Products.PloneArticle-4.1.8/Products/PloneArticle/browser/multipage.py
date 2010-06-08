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
Multipage views
"""

__docformat__ = 'restructuredtext'

# Zope imports
from zope.interface import Interface, implements
from Products.Five import BrowserView
from Acquisition import aq_inner
from plone.app.layout.navigation.defaultpage import DefaultPage
from interface import IPloneArticleMultipageView
from Products.PloneArticle.interfaces import IPloneArticle
    
# class MultiPageDefaultPage(DefaultPage):
#     def getDefaultPage(self, context_=None):
#         """
#         Override Plone default implementation:
#         Use multipage default page
#         """
        
#         context = aq_inner(self.context)
#         return context.getDefaultPage()


class NonMultipageContext(BrowserView):
    """
    View for generic article containers (folders, ...)
    """
    implements(IPloneArticleMultipageView)

    def isMultipage(self):
        return False

    def getPages(self):
        raise ValueError, "not in a multipage article"

    def getTOCItems(self, context=None):
        raise ValueError, "not in a multipage article"

    def getPreviousPage(self, context):
        raise ValueError, "not in a multipage article"

    def getNextPage(self, context):
        raise ValueError, "not in a multipage article"

class PloneArticleMultipageView(BrowserView):
    """
    View for PloneArticleMultipage
    """
    implements(IPloneArticleMultipageView)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.pages = None

    ### IPloneArticleMultipageView #####################################

    def isMultipage(self):
        return True

    def getPages(self):
        pages = self.pages
        if pages is None:
            pages = self.pages = self.context.getPages()
        return pages

    def getTOCItems(self, context=None):
        
        current_article_id = (context is not None) and context.getId()
        pages = self.getPages()
        pages_list = []
        
        for page in pages:
            page_id = page.getId
            is_selected = current_article_id and (page_id == current_article_id)
            item = {
                'id': page_id,
                'title': page.Title,
                'url': page.getURL(),
                'selected': is_selected,
                }
            pages_list.append(item)

        return pages_list

    def getPreviousPage(self, context):
        context_id = context.getId()
        pages = self.getPages()
        idx = self._getPageIndex(pages, context_id)

        # idx is None or 0
        if not idx:
            return None
        
        return pages[idx - 1]

    def getNextPage(self, context):
        context_id = context.getId()
        pages = self.getPages()
        idx = self._getPageIndex(pages, context_id)

        if idx is None or (idx+1 >= len(pages)):
            return None
        return pages[idx + 1]

    ### private methods ################################################

    def _getPageIndex(self, pages, page_id):
        pages_id = [p.getId for p in pages]
        try:
            idx = pages_id.index(page_id)
        except ValueError:
            return None
        return idx
