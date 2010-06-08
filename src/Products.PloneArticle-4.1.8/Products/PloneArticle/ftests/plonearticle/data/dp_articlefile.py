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
# $Id: dp_articlefile.py 5793 2007-01-29 09:47:52Z roeder $
from funittest import DataProvider

class ArticleFile(DataProvider):
    pass
    
default = {'new_file_title':'An article',
           'new_file_description':'An article description',
           'new_file':'/Users/maik/Projects/funittest/README.txt'}
           
key="new_file_title"
articlefile = ArticleFile("PloneArticle", default, key)

provide = articlefile.provide

provide({'new_file_title':'File 1',
         'new_file_description':"File 1 Description"})
