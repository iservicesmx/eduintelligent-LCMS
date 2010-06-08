# -*- coding: utf-8 -*-
## This module contains all content types used in PloneArticle product
## Copyright (C)2005 Ingeniweb

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
This module is an example of how to inherit from PloneArticle.

It adds a "location" field, which is a simple text field.

"""

__docformat__ = 'restructuredtext'

# Python imports
from copy import deepcopy

# Zope imports
from AccessControl import ClassSecurityInfo

# CMF imports

# Archetypes imports
try:
    from Products.LinguaPlone.public import registerType, Schema, StringField
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import registerType, Schema, StringField

from Products.PloneArticle.content.article import PloneArticle, PloneArticleSchema

from Products.PloneArticle import config

# Inherits schema from PloneArticle
# Copy it to make sure PloneArticle schema is totally independant
ArticleWithLocationSchema = PloneArticleSchema.copy() + Schema((
    StringField(
        'location',
        schemata='misc',
        ),
    ),)

# Inherits actions from PloneArticle
# Copy them to make sure ArticleWithLocation actions are totally independant
ArticleWithLocationActions = deepcopy(PloneArticle.actions)

class ArticleWithLocation(PloneArticle):
    """
        An article with a location field
    """

    # Standard content type setup
    portal_type = meta_type = 'ArticleWithLocation'
    archetype_name = 'Article with location'
    content_icon = 'plonearticle.gif'
    schema = ArticleWithLocationSchema
    typeDescription = 'An article with a location field'
    typeDescMsgId = 'description_edit_articlewithlocation'

    # Set up our views - these are available from the 'display' menu
#    default_view = 'pa_model1'
#    immediate_view = 'pa_model1'
#    suppl_views = (
#        'pa_model2',
#        'pa_model3',
#        'pa_model4',
#        'pa_model5',
#        'pa_model6',
#        'pa_model7',
#        'pa_model8',
#        'pa_model9',
#        'pa_model10',
#        )

    # Make sure we get title-to-id generation when an object is created
    _at_rename_after_creation = True

    # Get the standard actions (tabs)
    actions = ArticleWithLocationActions
    security = ClassSecurityInfo()

registerType(ArticleWithLocation, config.PROJECTNAME)
