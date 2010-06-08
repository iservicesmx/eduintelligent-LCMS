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
This module contains all content types used in PloneArticle product
"""

__docformat__ = 'restructuredtext'

# Zope imports
from AccessControl import ClassSecurityInfo
from zope.interface import implements
from zope import event

# CMF imports
from Products.CMFCore import permissions as CCP
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.event import ObjectInitializedEvent
from Products.Archetypes.event import ObjectEditedEvent
from Products.Archetypes.utils import mapply

try:
    from Products.LinguaPlone.public import registerType, Schema
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import registerType, Schema

# Products imports
from Products.ATContentTypes.content.document import ATDocument, \
     ATDocumentSchema

from Products.PloneArticle.config import PLONEARTICLE_TOOL

from Products.PloneArticle.interfaces import IPloneArticle
from Products.PloneArticle.field import FileInnerContentField, \
     ImageInnerContentField, LinkInnerContentField
from Products.PloneArticle.widget import FileInnerContentWidget, \
    ImageInnerContentWidget, LinkInnerContentWidget
from Products.PloneArticle.content.mixin import ArticleMixin
from Products.PloneArticle.pafti import PloneArticleFactoryTypeInformation

from Products.PloneArticle.version import CURRENT_ARTICLE_VERSION


# Inherits schema from ATDocument
# Copy it to make sure PloneArticle schema is totally independant
PloneArticleSchema = ATDocumentSchema.copy() + Schema((
    FileInnerContentField(
        'files',
        searchable=True,
        schemata='files',
        widget=FileInnerContentWidget(
            label='Files',
            label_msgid='label_files',
            i18n_domain='plonearticle',
            ),
        ),
    ImageInnerContentField(
        'images',
        searchable=True,
        schemata='images',
        widget=ImageInnerContentWidget(
            label='Images',
            label_msgid='label_images',
            i18n_domain='plonearticle',
            ),
        ),
    LinkInnerContentField(
        'links',
        searchable=True,
        schemata='links',
        widget=LinkInnerContentWidget(
            label='Links',
            label_msgid='label_links',
            i18n_domain='plonearticle',
            ),
        ),
    ),)

# We need to change the order of schematas such we got default, files, image, links, others...

PloneArticleSchema.moveField('files', after='text')
PloneArticleSchema.moveField('images', after='files')
PloneArticleSchema.moveField('links', after='images')


_marker = []

class PloneArticle(ArticleMixin, ATDocument):
    """A rich document containing files, images, links"""

    implements(IPloneArticle)

    # FIXME: We need to add this Zope 2 interface because the Archetypes tool
    # doesn't care about Zope 3 interfaces. Feature or bug?
    __implements__ = ATDocument.__implements__

    # Standard content type setup
    schema = PloneArticleSchema
    typeDescMsgId = 'description_edit_plonearticle'

    _at_fti_meta_type = PloneArticleFactoryTypeInformation.meta_type

    # Make sure we get title-to-id generation when an object is created
    _at_rename_after_creation = True

    # Enable marshalling via WebDAV/FTP/ExternalEditor.
    __dav_marshall__ = True

    __pa_version = ()

    # Get the standard actions (tabs)
    security = ClassSecurityInfo()

    security.declareProtected(CCP.ModifyPortalContent, 'initializeArchetype')
    def initializeArchetype(self, **kwargs):
        """called by the generated add* factory in types tool

        Overwritten to call the 'right' initializeArchetype and set PA version
        number at creation time.
        """
        ATDocument.initializeArchetype(self, **kwargs)

        self.__pa_version = CURRENT_ARTICLE_VERSION

    security.declareProtected(CCP.ManagePortal, 'getPAVersion')
    def getPAVersion(self):
        """Return the version used to create this article
        """
        return self.__pa_version

    security.declareProtected(CCP.ManagePortal, 'setPAVersion')
    def setPAVersion(self, version):
        """Set the version used to create this article. Usually called after
        migration
        """
        self.__pa_version = version

    ### ISelectableBrowserDefault overrides ###
    def getAvailableLayouts(self):
        """Get the layouts from enabled models (configured by plonarticle_tool).
        """
        tool = getToolByName(self, PLONEARTICLE_TOOL)
        models = tool.getModelRegistry()
        model_ids, default = tool.getEnabledModelsForType(self.aq_explicit.portal_type)
        result = []
        for mid in model_ids:
            model = models.get(mid, None)
            if model is None:
                continue
            result.append((mid, model.Title()))

        return result

    def canSetDefaultPage(self):
        """
        Override BrowserDefaultMixin because default page stuff doesn't make
        sense for articles.
        """
        return False       
    
    security.declarePrivate('_processForm')
    def _processForm(self, data=1, metadata=None, REQUEST=None, values=None):
        """BaseObject._processForm override 
          this patch is done to make processForm possible by fieldset
          when IMultiPageSchema is not implemented
        """
    
        request = REQUEST or self.REQUEST
        if values:
            form = values
        else:
            form = request.form
              
        fieldset = form.get('fieldset', None)
        if fieldset is None :
            ArticleMixin._processForm(self, data=data, metadata=metadata,
                                      REQUEST=REQUEST, values=values)
        else :                  
            schema = self.Schema()
            schemata = self.Schemata()
            fields = []
    
            fields = schemata[fieldset].fields()                
    
            form_keys = form.keys()
    
            for field in fields:
    
                if not field.writeable(self):
    
                    continue
    
                widget = field.widget
                result = widget.process_form(self, field, form,
                                             empty_marker=_marker)
                if result is _marker or result is None: continue
    
                # Set things by calling the mutator
                mutator = field.getMutator(self)
                __traceback_info__ = (self, field, mutator)
                result[1]['field'] = field.__name__
                mapply(mutator, result[0], **result[1])
    
            self.reindexObject()        

registerType(PloneArticle)
