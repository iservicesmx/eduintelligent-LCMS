# -*- coding: utf-8 -*-
## This module contains permissons used in PloneArticle product
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


# Zope imports
from Globals import InitializeClass
from Globals import DTMLFile
from AccessControl import ClassSecurityInfo

# CMF imports
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ManagePortal
from Products.CMFDynamicViewFTI.fti import DynamicViewTypeInformation
from Products.CMFCore.TypesTool import TypesTool, FactoryTypeInformation

# Products imports
from Products.PloneArticle import utils
from Products.PloneArticle.interfaces import IBaseInnerContent
from Products.PloneArticle.proxy.fileinnercontent import FileInnerContentProxy
from Products.PloneArticle.proxy.imageinnercontent import ImageInnerContentProxy
from Products.PloneArticle.proxy.linkinnercontent import LinkInnerContentProxy

fti_meta_type = 'Factory-based Type Information for Plone Articles content types'

class PloneArticleFactoryTypeInformation(DynamicViewTypeInformation):
    """FTI for PloneArticle based types options
        PloneArticle FactoryTypeInformation is a dynamic view FTI with some other
        properties enabling it to store PA options per content type in a clean way.

        Properties are :
        * referenceableAttachmentType
        * referenceableImageType
        * referenceableLinkType
        * attachmentMaxSize
        * imageMaxSize
        * previewAllowed
    """

    meta_type = fti_meta_type
    security = ClassSecurityInfo()

    referenceableAttachmentType = []
    _properties = DynamicViewTypeInformation._properties + (
        {
            'id': 'referenceableAttachmentType',
            'type': 'multiple selection',
            'mode': 'w',
            'label': 'Referenceable attachment type',
            'select_variable': 'getAvailableReferenceableAttachmentTypes',
        },
        {
            'id': 'referenceableImageType',
            'type': 'multiple selection',
            'mode': 'w',
            'label': 'Referenceable image type',
            'select_variable': 'getAvailableReferenceableImageTypes',
        },
        {
            'id': 'referenceableLinkType',
            'type': 'multiple selection',
            'mode': 'w',
            'label': 'Referenceable link type',
            'select_variable': 'getAvailableReferenceableLinkTypes',
        },
        {
            'id': 'attachmentMaxSize',
            'type': 'int',
            'mode': 'w',
            'label': 'Max size for attachment',
        },
        {
            'id': 'imageMaxSize',
            'type': 'int',
            'mode': 'w',
            'label': 'Max size for image',
        },
        {
            'id': 'previewAllowed',
            'type': 'boolean',
            'mode': 'w',
            'label': 'Is preview allowed?',
        },

    )

    referenceableAttachmentType = []
    referenceableImageType = []
    referenceableLinkType = []
    attachmentMaxSize = 3 * 2 ** 20
    imageMaxSize = 3 * 2 ** 20
    previewAllowed = True

    def manage_afterAdd(self, item, container):
        ## This method will only work with third party products. Base PloneArticle
        ## initialize the FTI with another method.
        try:
            paTool = getToolByName(self, 'plonearticle_tool')
        except AttributeError:
            return

        self.initializeFti(item)

    def initializeFti(self, item):
        """
            Initialize the FTI with default value
            This method can be called only when the PA tool is installed.
        """

        self.referenceableAttachmentType = getattr(self, 'referenceableAttachmentType', self.getAvailableReferenceableAttachmentTypes())
        self.referenceableImageType = getattr(self, 'referenceableImageType', self.getAvailableReferenceableImageTypes())
        self.referenceableLinkType = getattr(self, 'referenceableLinkType', self.getAvailableReferenceableLinkTypes())
        self.attachmentMaxSize = getattr(self, 'attachmentMaxSize', 3 * 2 ** 20)
        self.imageMaxSize = getattr(self, 'imageMaxSize', 3 * 2 ** 20)
        self.previewAllowed = getattr(self, 'previewAllowed', True)

    def getAvailableReferenceableAttachmentTypes(self):
        return utils.getAllAvailableReferenceableTypes(self, FileInnerContentProxy)

    def getAvailableReferenceableImageTypes(self):
        return utils.getAllAvailableReferenceableTypes(self, ImageInnerContentProxy)

    def getAvailableReferenceableLinkTypes(self):
        return utils.getAllAvailableReferenceableTypes(self, LinkInnerContentProxy)

InitializeClass(PloneArticleFactoryTypeInformation)


def manage_addPAFTIForm(self, REQUEST):
    """ Get the add form for factory-based type infos.
    """
    addTIForm = DTMLFile('addTypeInfo', _dtmldir).__of__(self)
    ttool = getToolByName(self, 'portal_types')
    return addTIForm( self, REQUEST,
                      add_meta_type=PloneArticleFactoryTypeInformation.meta_type,
                      types=ttool.listDefaultTypeInformation() )

class DynamicAllowedContentFTI(FactoryTypeInformation):
    """
    Allow content to be added if it implements BaseInnercontentProxy
    """

    meta_type = "DynamicAllowedContentFTI for InnerContentContainer"

    security = ClassSecurityInfo()

    security.declarePublic('allowType')
    def allowType(self, contentType):
        """
            Can objects of 'contentType' be added to containers whose
            type object we are?
        """
        atool = getToolByName(self, 'archetype_tool')
        types = [ti for ti in atool.listRegisteredTypes()
                 if ti['portal_type'] == contentType]
        return len(types) > 0 and \
               atool.typeImplementsInterfaces(types[0], (IBaseInnerContent,))

InitializeClass(DynamicAllowedContentFTI)

def manage_addDVTFTIForm(self, REQUEST):
    """ Get the add form for factory-based type infos.
    """
    addTIForm = DTMLFile('addTypeInfo', _dtmldir).__of__(self)
    ttool = getToolByName(self, 'portal_types')
    return addTIForm( self, REQUEST,
                      add_meta_type=PloneArticleFactoryTypeInformation.meta_type,
                      types=ttool.listDefaultTypeInformation() )

# BBB: the following lines are required to register the new FTI in CMF 1.5 and may
# be removed after switching to CMF 1.6
try:
    from Products.CMFCore.TypesTool import typeClasses
except ImportError:
    pass
else:

    setattr(TypesTool, 'manage_addPAFTIForm',
                        manage_addPAFTIForm)

    setattr(TypesTool, 'manage_addPAFTIForm__roles__',
                        ('Manager', ))

    typeClasses.append(
        {'class' : PloneArticleFactoryTypeInformation,
         'name' : PloneArticleFactoryTypeInformation.meta_type,
         'action': 'manage_addPAFTIForm',
         'permission' : ManagePortal,
         },
        )

    setattr(TypesTool, 'manage_addDVTFTIForm',
                        manage_addDVTFTIForm)

    setattr(TypesTool, 'manage_addDVTFTIForm__roles__',
                        ('Manager', ))

    typeClasses.append(
        {'class' : DynamicAllowedContentFTI,
         'name' : DynamicAllowedContentFTI.meta_type,
         'action': 'manage_addDVTFTIForm',
         'permission' : ManagePortal,
         },
        )
