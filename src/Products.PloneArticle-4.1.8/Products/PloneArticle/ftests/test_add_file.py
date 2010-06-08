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
# $Id: test_add_file.py 5781 2007-01-21 17:55:37Z roeder $
import unittest
from funittest import logical
from funittest import dataprovider
from funittest import precondition
from funittest import interpreter
from funittest import TestCase

import os

class TestAddFile(TestCase):

    def setUp(self):    
        TestCase.setUp(self)
        interpreter.open("")        
        user=dataprovider.cmfplone.user.get('sampleadmin')
        logical.cmfplone.application.change_user(user)        
        self.article = dataprovider.plonearticle.article.get("Article 1")
        precondition.plonearticle.article.existing_article(self.article)

    def test_add_file(self):
        "Add a file to an article"
        interpreter.annotate("Test: Add a file to the article")
        file = dataprovider.plonearticle.articlefile.get("File 1")
        logical.plonearticle.article.add_file(file)
        logical.plonearticle.article.save_article(self.article)
        
if __name__ == "__main__":
    unittest.main()
