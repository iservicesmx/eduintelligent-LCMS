# -*- coding: utf-8 -*-
## 
## Copyright (C) 2008 Ingeniweb

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
"""
Plone Article migration module from 4.0 to 4.1 betas
"""
__version__ = "$Revision:  $"
# $Source:  $
# $Id:  $
__docformat__ = 'restructuredtext'

from Products.PloneArticle.migration import applyArticles


def stable40x_410beta1(portal):

    out = []

    def modifyMetaTypes(article):
        # Change meta_type of xxxinnercontentproxy subobjects
        old_mts_to_news = {
            'FileContentInnerProxy': 'FileInnerContentProxy',
            'ImageContentInnerProxy': 'ImageInnerContentProxy',
            'LinkContentInnerProxy': 'LinkInnerContentProxy'
            }
        old_mts = old_mts_to_news.keys()
        for icc in article.objectValues(spec='InnerContentContainer'):
            for item in icc.objectValues():
                mt = item.meta_type
                if mt in old_mts:
                    item.meta_type = old_mts_to_news[mt]
        return

    applyArticles(portal, modifyMetaTypes)
    out.append("Changed meta_type of inner items")
    return out
