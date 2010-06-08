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
# $Id: test_add_image.py 5836 2007-02-08 13:17:49Z roeder $
import unittest
from funittest import logical
from funittest import physical
from funittest import dataprovider
from funittest import precondition
from funittest import interpreter
from funittest import TestCase

import os

class TestAddImage(TestCase):

    def setUp(self):    
        TestCase.setUp(self)
        interpreter.open("")        
        user=dataprovider.cmfplone.user.get('sampleadmin')
        logical.cmfplone.application.change_user(user)        
        self.article = dataprovider.plonearticle.article.get("Article 1")
        precondition.plonearticle.article.existing_article(self.article)

    def test_add_image(self):
        "Add an image to an article and save the article"
        interpreter.annotate("Test: Add an image to the article and save the article")
        image = dataprovider.plonearticle.articleimage.get("Image 1")
        # Normal attachment upload
        logical.plonearticle.article.add_image(image)
        logical.plonearticle.article.save_article(self.article)

    def test_add_non_existing_image(self):
        "Try adding a non-existing image to an article"
        interpreter.annotate("Test: Try adding a non-existing image to an article")
        image = dataprovider.plonearticle.articleimage.get("Non-existing Image")
        physical.cmfplone.tab.access("edit")
        physical.cmfplone.schemata.access("images")
        physical.plonearticle.attachment_upload.access()
        physical.plonearticle.attachment_upload.fill(image)
        physical.plonearticle.attachment_upload.save(image, "error")        
        interpreter.verifyTextPresent("Image upload error: cannot identify image file")
        # Due to differences in the *chrome mode, the following error is not produced:
        # interpreter.verifyTextPresent("Error: Zero file size")
        physical.plonearticle.attachment_upload.cancel()  
        logical.plonearticle.article.save_article(self.article)
        
    def test_cancel_adding_an_image(self):
        "Cancel adding an image"
        interpreter.annotate("Test: Add an image to the article and cancel")
        image = dataprovider.plonearticle.articleimage.get("Image 1")
        physical.cmfplone.tab.access("edit")
        physical.cmfplone.schemata.access("images")
        physical.plonearticle.attachment_upload.access()
        physical.plonearticle.attachment_upload.fill(image)
        # Not saving here.
        physical.plonearticle.attachment_upload.cancel()  
        logical.plonearticle.article.save_article(self.article)

    def test_add_two_images_and_change_position(self):
        "Add two images and change their position"
        interpreter.annotate("Test: Add two images and change their position")

        images = []
        images.append(dataprovider.plonearticle.articleimage.get("Image 1"))
        images.append(dataprovider.plonearticle.articleimage.get("Image 2"))
        logical.plonearticle.article.add_multiple_images(images)

        # Change position of images       
        interpreter.click("//a[@class='file_move_down'][1]")
        interpreter.click("//a[@class='file_move_down'][1]")
        logical.plonearticle.article.save_article(self.article)
        
if __name__ == "__main__":
    unittest.main()
