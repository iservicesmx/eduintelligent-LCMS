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
# $Id: test_delete_file.py 5783 2007-01-21 17:59:47Z roeder $
import unittest
from funittest import logical
from funittest import dataprovider
from funittest import scripts
from funittest import interpreter
from funittest.testrunner import Test
from funittest import Schema
from funittest import register_tst

import os

class DeleteFile(Test):
    schema = Schema()

    _uses_file_upload = 1

    def setUp(self):    
        interpreter.open("")        
        user=dataprovider.cmfplone.user.get('sampleadmin')
        logical.cmfplone.application.login(user)        
        self.article = dataprovider.plonearticle.article.get("article1")
        files = [dataprovider.plonearticle.articlefile.get("File 1"),]
        images = []
        links = []
        scripts.plonearticle.article.existing_article_with_attachments(self.article, files, images, links)

    def step_1(self):
        file = dataprovider.plonearticle.articlefile.get("File 1")
        "Delete a file in an article"
        logical.plonearticle.article.delete_file(file)
        logical.plonearticle.article.save_article(self.article)

    def test(self):
        self.expect_ok(1)

register_tst("PloneArticle", DeleteFile())
