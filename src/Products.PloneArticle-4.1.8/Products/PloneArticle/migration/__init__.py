# -*- coding: utf-8 -*-
## Copyright (C) 2006 Ingeniweb

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

import sys
import transaction
import itertools

# Zope imports
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem

from Products.CMFCore.utils import getToolByName

from Products.PloneArticle import tool, content


# Module aliases needed for migration
class Dummy:
    pass


class OrderedList(SimpleItem):
    """Ordered list with unique elements"""

    security = ClassSecurityInfo()

    security.declarePrivate('__init__')
    def __init__(self):
        """Initialize list"""
        self.olist = []

    security.declarePrivate('add')
    def add(self, items):
        """Add new items"""
        for item in items:
            self.olist.append(item)

        self.olist = self.olist

    security.declarePrivate('remove')
    def remove(self, items):
        """Remove items"""
        for item in items:
            self.olist.remove(item)

        self.olist = self.olist

    security.declarePrivate('moveByDelta')
    def moveByDelta(self, items, delta):
        """Move items by delta"""

        for item in items:
            index = self.olist.index(item) - delta
            self.olist.remove(item)
            self.olist.insert(index, item)

        self.olist = self.olist

    security.declarePrivate('getItems')
    def getItems(self):
        """Get all items"""
        return self.olist

InitializeClass(OrderedList)

import new
attachmentmixin = new.module('AttachmentMixin')
attachmentmixin.AttachmentReferenceBrain = Dummy
attachmentmixin.OrderedList = OrderedList
attachmentmixin.AttachmentContents = Dummy

articlecore = new.module('ArticleCore')
articlecore.ArticleCore = Dummy
articlecore.ArticleReferenceBrain = Dummy

sys.modules['Products.PloneArticle.PloneArticle'] = content.article
sys.modules['Products.PloneArticle.PloneArticleMultiPage'] = content.multipage
sys.modules['Products.PloneArticle.PloneArticleTool'] = tool
sys.modules['Products.PloneArticle.AttachmentMixin'] = attachmentmixin
sys.modules['Products.PloneArticle.ArticleCore'] = articlecore

def applyArticles(portal, func, portal_type='PloneArticle',
                  savepoint_interval=100):
    """
    Apply a function on all articles

    @param portal_type: a string or list of strings for types to look for

    @param savepoint_interval: do a savepoint(optimistic) every 'interval'
    processed content
    """

    savepoint = transaction.savepoint
    portal_catalog = getToolByName(portal, 'portal_catalog')
    article_brains = portal_catalog(portal_type=portal_type)

    for brain, count in itertools.izip(article_brains, itertools.count()):
        article = brain.getObject()
        #FIXME: is article = None possible?
        func(article)

        if count % savepoint_interval:
            savepoint(optimistic=True)

    return

#####################################


def null(portal):
    """ This is a null migration, use it when nothing happens """
    pass

def executeMigrations():
    from Products.PloneArticle.migration import v4
    from Products.PloneArticle.migration import v4_1

def registerMigrations():

    tool.registerUpgradePath('3.2.99', '4.0.0-beta1', v4.betas.v3_v4beta1)
    tool.registerUpgradePath('4.0.0-beta1', '4.0.0-beta2', null)
    tool.registerUpgradePath('4.0.0-beta2', '4.0.0-beta3', null)
    tool.registerUpgradePath('4.0.0-beta3', '4.0.0-beta4', v4.betas.beta3_beta4)
    tool.registerUpgradePath('4.0.0-beta4', '4.0.0-beta5', null)
    tool.registerUpgradePath('4.0.0-beta5', '4.0.0-beta6', v4.betas.beta5_beta6)
    tool.registerUpgradePath('4.0.0-beta6', '4.0.0-rc1', null)
    tool.registerUpgradePath('4.0.0-rc1', '4.0.0-rc2', null)
    tool.registerUpgradePath('4.0.0-rc2', '4.0.0-rc3', null)
    tool.registerUpgradePath('4.0.0-rc3', '4.0.0-rc4', null)
    tool.registerUpgradePath('4.0.0-rc4', '4.0.0-rc5', null)
    tool.registerUpgradePath('4.0.0-rc5', '4.0.0-rc6', null)
    tool.registerUpgradePath('4.0.0-rc6', '4.0.0', null)
    tool.registerUpgradePath('4.0.0', '4.0.1', null)
    tool.registerUpgradePath('4.0.1', '4.0.2', null)
    tool.registerUpgradePath('4.0.2', '4.0.3', null)
    tool.registerUpgradePath('4.0.3', '4.0.4', null)
    tool.registerUpgradePath('4.0.4', '4.1.0-beta1', v4_1.betas.stable40x_410beta1)
    tool.registerUpgradePath('4.1.0-beta1', '4.1.0-beta2', null)
    tool.registerUpgradePath('4.1.0-beta2', '4.1.0-beta3', null)
    tool.registerUpgradePath('4.1.0-beta3', '4.1.0-RC1', null)
    tool.registerUpgradePath('4.1.0-RC1', '4.1.0-RC2', null)
    tool.registerUpgradePath('4.1.0-RC2', '4.1.0-final', null)
    tool.registerUpgradePath('4.1.0-final', '4.1.1', null)
    tool.registerUpgradePath('4.1.1', '4.1.2', null)
    tool.registerUpgradePath('4.1.2', '4.1.3', null)
    tool.registerUpgradePath('4.1.3', '4.1.4', null)
    tool.registerUpgradePath('4.1.4', '4.1.5', null)
    tool.registerUpgradePath('4.1.5', '4.1.6', null)
    tool.registerUpgradePath('4.1.6', '4.1.7', null)
    tool.registerUpgradePath('4.1.7', '4.1.8', null)
    return

