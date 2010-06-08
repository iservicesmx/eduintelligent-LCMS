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

from funittest import interpreter
from funittest import register_pom

class AttachmentBrowse:
    """
    When the user edits an article, he can access the different attachments,
    image, link and file.
    The user can click on the browse button to add an attachment to the
    article, which already exists somewhere in the site.
    The browse form is the same for the different attachment types, so
    this model is designed to be reusable.
    """
    def access(self):
        """
        Access the browse view by clicking on the browse link.
        """
        interpreter.click("plone-article-browse-link")        
        # XXX Wait for condition!
                
register_pom("PloneArticle", AttachmentBrowse())
