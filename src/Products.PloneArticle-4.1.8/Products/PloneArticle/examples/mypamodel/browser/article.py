# -*- coding: utf-8 -*-
## Copyright (C)2007 Ingeniweb

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
Our view classes
$Id$
"""

from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView

# Root view class for PloneArticle (Five.BrowseView subclass)
from Products.PloneArticle.browser.article import PloneArticleModelView

# Unregistered viws are useless ;)
from Products.PloneArticle.model import registerArticleModel

# Importing our model interfaces
from interface import IPAViewWithAuthor

# You should now take a look at Products/PloneArticle/browser/article.py
# to see what's already publicly available.
# Other points of interest for your view class are:
# * ATDocument of ATContentTypes: PloneArticle inherits from this type
# * Products/PloneArticle/content/*.py: PloneArticle schema and resources
# * Products/PloneArticle/field/*.py: How we access inner content (files, images)

class PAViewWithAuthor(PloneArticleModelView):
    # Note that the docstring is used as default description of our model.
    """
    Like the documentation view, but adds the portrait of the author
    at the top left of the article.
    """

    implements(IPAViewWithAuthor)

    template_id = 'author_pa_model' # Your layer directory must have 'my_pa_model.pt'
    title = u"Documentation model with author portrait" # Always Unicode and english
    title_msgid = 'author_model_title' # See mypamodel/i18n
    description_msgid = 'author_model_description' # See mypamodel/i18n/*
    icon = 'author_pa_model.png' # Your layer directory must have this picture

    def authorInfo(self):
        """
        See IPAViewWithAuthor
        """

        context = self.context
        portal_membership = getToolByName(context, 'portal_membership')
        portal_url = getToolByName(context, 'portal_url')()
        creator = context.Creator()
        info = portal_membership.getMemberInfo(creator)
        return {
            'fullname': info and info['fullname'] or creator,
            'url': '%s/author/%s' % (portal_url, creator),
            'portrait': portal_membership.getPersonalPortrait(creator)
            }
        


# Unregistered views cannot selected by author
registerArticleModel(PAViewWithAuthor)
