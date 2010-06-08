# -*- coding: utf-8 -*-
## PloneArticle
## A Plone document incorporating images, attachments and links, whith a free choice of layout.
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
# $Id: dp_articlelink.py 5766 2007-01-15 16:52:32Z roeder $
from funittest import DataProvider

class ArticleLink(DataProvider):
    pass
    
default = {'new_title':'An article link',
           'new_description':'An article link description',
           'new_url':'http://www.plone.org',}

key="new_title"
articlelink = ArticleLink("PloneArticle", default, key)

provide = articlelink.provide

provide({'new_title':'Link 1',
         'new_description':"Link 1 Description",
         'new_url':'http://www.plone.org'})

        
        