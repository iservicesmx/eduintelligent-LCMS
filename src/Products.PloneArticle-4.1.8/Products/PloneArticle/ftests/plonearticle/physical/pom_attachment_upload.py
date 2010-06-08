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

class Attachment_Upload:
    """
    When the user edits an article, he can access the different attachments,
    image, link and file.
    The user can click on the upload button to add an attachment to the
    article.
    The upload form is the same for the different attachment types, so
    this model is designed to be reusable.
    """
    
    def add(self, attach, postcondition="success"):
        """
        The user is inside the attachment view of an article. He wants to
        upload an attachment. The procedure is always the same for images,
        files and links.
        
        - attach: The attachment to add (image, link or file)
        - postcondition: "success" or "error" depending on the expectation
        """        
        # The user fills in the upload form
        self.fill(attach)
        # The user saves the upload form
        self.save(attach, postcondition)
        # The user has to use the cancel button if he doesn't want to add any more attachments
        self.cancel()    

    def access_links(self):
        """
        Access the upload view by clicking on the upload link.
        """
        interpreter.click("//div[@id='archetypes-fieldname-links']//a[@id='plone-article-upload-link']")
        interpreter.wait_for_condition("selenium.isElementPresent('new_file_btn_ok');",10000)    

    def access_images(self):
        """
        Access the upload view by clicking on the upload link.
        """
        interpreter.click("//div[@id='archetypes-fieldname-images']//a[@id='plone-article-upload-link']")
        interpreter.wait_for_condition("selenium.isElementPresent('new_file_btn_ok');",10000)    

    def access_files(self):
        """
        Access the upload view by clicking on the upload link.
        """
        interpreter.click("//div[@id='archetypes-fieldname-files']//a[@id='plone-article-upload-link']")
        interpreter.wait_for_condition("selenium.isElementPresent('new_file_btn_ok');",10000)    
        
    def fill(self, form):
        """
        Fill in the attachment form generically.
        """
        for key, value in form.items():
            interpreter.type(key, value)

    def save(self, attach, postcondition="success"):        
        """
        Save the attachment.
        
        Postcondition can be "success" or "error"
        """
        interpreter.click("new_file_btn_ok")
        if postcondition=="success":
            interpreter.wait_for_condition("selenium.isElementPresent('upload-status-success');",10000)    
        elif postcondition=="error":
            interpreter.wait_for_condition("selenium.isElementPresent('upload-status-error');",10000)
            # In case of an error, the title and description should not be lost
            interpreter.failUnless(interpreter.get_value("//input[@id='new_file_title']")==attach['new_file_title'])            
            interpreter.failUnless(interpreter.get_value("//input[@id='new_file_description']")==attach['new_file_description'])            
            
    def cancel(self):
        """
        Cancel the upload form, and return to the attachment form.
        """
        interpreter.click("btnCancel")

register_pom("PloneArticle", Attachment_Upload())
