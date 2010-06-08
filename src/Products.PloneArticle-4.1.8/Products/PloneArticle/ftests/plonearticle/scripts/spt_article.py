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
# $Id: pc_article.py 5777 2007-01-21 17:20:27Z roeder $

from funittest import physical
from funittest import logical
from funittest import interpreter
from funittest import dataprovider
from funittest import register_spt
from funittest import Testable
import random
import os

class Article:

    def existing_article(self, article):        
        interpreter.annotate("Setup article")
        logical.cmfplone.navigation.top()
        logical.cmfplone.folder.add(article)
        logical.cmfplone.content.edit(article)        
        logical.cmfplone.content.save(article)

    def existing_article_without_attachments(self, article):        
        interpreter.annotate("Setup article")
        self.existing_article(article)
        # Need to delete all images
        for attachment_type in ["images", "files", "links"]:
            physical.cmfplone.tab.access("edit")
            physical.cmfplone.schemata.access(attachment_type)
            i = 0
            while interpreter.is_element_present("//div[@id='%s-innercontent%06d']" % (attachment_type, i)):
                interpreter.click("//div[@id='%s-innercontent%06d']/div/a[@class='file_delete']" % (attachment_type, i))
                i+=1
                #os.system("pause")
            logical.cmfplone.content.save(article)
        #os.system("pause")
        
    def existing_article_with_attachments(self, article, files, images, links):
        self.existing_article_without_attachments(article)
        if files:
            for file in files:
                logical.plonearticle.article.add_file(file)
        if images:
            for image in images:
                logical.plonearticle.article.add_image(image)
        if links:
            for link in links:
                logical.plonearticle.article.add_link(link)        
        logical.plonearticle.article.save_article(article)    
        
register_spt("PloneArticle", Article())

