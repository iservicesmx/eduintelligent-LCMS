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
# $Id: lfm_article.py 5834 2007-02-08 13:16:33Z roeder $
from funittest import logical
from funittest import interpreter
from funittest import physical
from funittest import dataprovider
from funittest import register_lfm
from funittest import Testable
import random
import os

class Article(Testable):
    """
    Articles can have three types of attachments:
    
    files, images and links
    
    These attachments can be uploaded in the same way.
    """
    def add_file(self, file, postcondition="success"):
        interpreter.annotate("Add a file to the article")
        physical.cmfplone.tab.access("edit")
        physical.cmfplone.schemata.access("files")
        physical.plonearticle.attachment_upload.add(file, postcondition)

    def add_image(self, image, postcondition="success"):
        interpreter.annotate("Add an image to the article")
        physical.cmfplone.tab.access("edit")
        physical.cmfplone.schemata.access("images")
        physical.plonearticle.attachment_upload.add(image, postcondition)

    def add_multiple_images(self, images):
        start=1
        for image in images:
            if start:
                physical.cmfplone.tab.access("edit")
                physical.cmfplone.schemata.access("images")
                physical.plonearticle.attachment_upload.access()
                physical.plonearticle.attachment_upload.fill(image)
                physical.plonearticle.attachment_upload.save(image)
                start=0
            else:                
                physical.plonearticle.attachment_upload.fill(image)
                physical.plonearticle.attachment_upload.save(image)
        # Leave upload
        physical.plonearticle.attachment_upload.cancel()     
        
    def add_link(self, link, postcondition="success"):
        interpreter.annotate("Add a link to the article")
        physical.cmfplone.tab.access("edit")
        physical.plonearticle.attachment_upload.access_links()
        physical.plonearticle.attachment_upload.add(link, postcondition)

    def save_article(self, article):
        logical.cmfplone.content.save(article)            

    def browse_file(self, file):
        interpreter.annotate("Browse for a file to be added to the article")
        physical.cmfplone.tab.access("edit")
        physical.cmfplone.schemata.access("files")
        physical.plonearticle.attachmentbrowse.access()
        # To be continued...
        
    def browse_image(self, image):
        interpreter.annotate("Browse for an image to be added to the article")
        physical.cmfplone.tab.access("edit")
        physical.cmfplone.schemata.access("images")
        physical.plonearticle.attachmentbrowse.access()
        # To be continued...

    def browse_link(self, link):
        interpreter.annotate("Browse for a link to be added to the article")
        physical.cmfplone.tab.access("edit")
        physical.cmfplone.schemata.access("links")
        physical.plonearticle.attachmentbrowse.access()
        # To be continued...

    def delete_file(self, file):
        interpreter.annotate("Delete a file from the article")
        physical.cmfplone.tab.access("edit")
        physical.cmfplone.schemata.access("files")
        # To be continued        
        
register_lfm("PloneArticle", Article())
