# -*- coding: utf-8 -*-
## Product description
##
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
"""
Multi-page content type stuff
"""

# Zope imports
from AccessControl import ClassSecurityInfo
from zope.interface import implements

# CMF imports
from Products.CMFCore import permissions as CCP
from Products.CMFCore.utils import getToolByName

# Archetypes imports
try:
    from Products.LinguaPlone.public import registerType, Schema
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import registerType, Schema

from Products.Archetypes.Field import BooleanField, ReferenceField
from Products.Archetypes.Widget import BooleanWidget

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget

from Products.ATContentTypes.content.folder import ATFolder

from Products.PloneArticle.interfaces import IPloneArticleMultiPage


schema = ATFolder.schema.copy() \
         + Schema((
    BooleanField(
        'viewTOCFirst',
        default=False,
        widget=BooleanWidget(
            label='View table of contents first',
            label_msgid='label_view_toc_first',
            i18n_domain='plonearticle',
            visible={'view' : 'invisible'},
        )
    ),
    BooleanField(
        'viewTOC',
        default=True,
        widget=BooleanWidget(
            label='Display table of contents in dropdown list',
            label_msgid='label_display_toc_dropdown',
            description='If you have checked properties to view TOC first, this property will not be applied.',
            description_msgid='description_display_toc_dropdown',
            i18n_domain='plonearticle',
            visible={'view' : 'invisible'},
        )
    ),
    ReferenceField(
        'evaluationDependecy',
        relationship='evaluation_dependecy',
        allowed_types=('Exam',),
        multiValued=False,
        #keepReferencesOnCopy=True,
        widget=ReferenceBrowserWidget(
            label='Referenced Evaluation',
            label_msgid='label_referenced_evaluation',
            i18n_domain='plonearticle',
            ),
        ),
    
    ))


class PloneArticleMultiPage(ATFolder):
    """ A folder containing articles """

    implements(IPloneArticleMultiPage)

    typeDescMsgId = 'description_edit_multipage'
    schema = schema

    security = ClassSecurityInfo()

    # Make sure we get title-to-id generation when an object is created
    _at_rename_after_creation = True

    security.declareProtected(CCP.View, 'getPages')
    def getPages(self, full_objects=False):
        """
        Return the ordered list of articles as brains
        """

        catalog = getToolByName(self, 'portal_catalog')
        mtool = getToolByName(self, 'portal_membership')

        show_inactive = mtool.checkPermission('Access inactive portal content', self)

        path = {'query': '/'.join(self.getPhysicalPath())
                ,'depth': 1
                }

        return catalog(path = path
                       ,sort_on='getObjPositionInParent'
                       ,show_all=1
                       ,show_inactive=show_inactive)



        #return self.getFolderContents(full_objects)

    security.declareProtected(CCP.View, 'getViewTOC')
    def getViewTOC(self):
        """Returns true if you can access TOC in dropdown menu"""

        field = self.getField('viewTOC')
        value = field.get(self)

        if not value and not self.getViewTOCFirst():
            return False

        return True


    security.declarePublic('canSetDefaultPage')
    def canSetDefaultPage(self):
        """
        Always False: the default page is automatic for multipage
        """
        return False

    security.declareProtected(CCP.View, 'getPAMDefaultPage')
    def getPAMDefaultPage(self):
        """
        Return the first user visible article as default page if
        ViewTOC is unchecked (i.e, it redirect the user to the first page)
        """

        request = getattr(self, 'REQUEST', None)
        force_toc = request.get('force_toc', False)
        pages = self.getPages()

        if force_toc or self.getViewTOCFirst() or len(pages) == 0:
            return ATFolder.__call__(self)
        else:
            return request.RESPONSE.redirect(pages[0].getObject().absolute_url())

    security.declareProtected(CCP.View, 'canViewModule')
    def canViewModule(self):
        """
        """
        # comprobar si tiene asociado un examen
        
        mtool = getToolByName(self, 'portal_membership')
        user = mtool.getAuthenticatedMember().getId()
        evaluation = self.getEvaluationDependecy()
        if evaluation:
            return evaluation.passEvaluation(user)
        return True



registerType(PloneArticleMultiPage)
