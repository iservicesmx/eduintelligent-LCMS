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
from funittest import scripts
from funittest import interpreter
from funittest import scenarios
from funittest.scenariorunner import Scenario
from funittest.testrunner import Test
from funittest import Schema
from funittest import register_sce

import os

class AddFile(Scenario):
    """
    Add a file to an article
    
    Preparation:
    
    1. Choose a user
    2. Choose a context
    3. Choose an article
    3. Choose a file for the article

    Use Case:
    
    1. Add file to article
    2. Save article
    """

    schema = Schema({"user":dataprovider.cmfplone.user,
                     "context":dataprovider.cmfplone.context,
                     "article":dataprovider.plonearticle.article,
                     "articlefile":dataprovider.plonearticle.articlefile,
                     })

    _uses_file_upload = 1

    def setUp(self):
        scenarios.cmfplone.login(user = self._user)
        scenarios.cmfplone.navigateto(context = self._context)
        scenarios.cmfplone.addcontent(content = self._article)

    def step_1(self):
        logical.plonearticle.article.add_file(self._articlefile)
    
    def step_2(self):
        logical.plonearticle.article.save_article(self._article)

    def scenario(self):
        """
        Add a file to an article
        """
        self.expect_ok(1,2)

register_sce("PloneArticle", AddFile())
