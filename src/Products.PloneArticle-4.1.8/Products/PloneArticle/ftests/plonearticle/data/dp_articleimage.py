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
# $Id: dp_articleimage.py 5793 2007-01-29 09:47:52Z roeder $
from funittest import DataProvider

class ArticleImage(DataProvider):
    pass
    
default = {'new_file_title':'An article image',
           'new_file_description':'An article image description',
           'new_file':"/Users/maik/Projects/funittest/media/plone_snow.jpg"}
key="new_file_title"
articleimage = ArticleImage("PloneArticle", default, key)

provide = articleimage.provide

provide({'new_file_title':'Image 1',
         'new_file_description':"Image 1 Description"})

provide({'new_file_title':'Image 2',
         'new_file_description':"Image 1 Description",
         'new_file':'/Users/maik/Projects/funittest/media/plone_cookies.jpg'})
        
provide({'new_file_title':'Non-existing Image',
         'new_file_description':"Non-existing Image",
         'new_file':"/Users/maik/Projects/funittest/media/plone_duct_cover.jpg"})
        
        
