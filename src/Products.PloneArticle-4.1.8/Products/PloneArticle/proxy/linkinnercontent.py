# -*- coding: utf-8 -*-
## Defines LinkInnerContentField
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
Defines LinkInnerContentProxy
"""

__docformat__ = 'restructuredtext'

# Zope imports
from AccessControl import ClassSecurityInfo
from zope.interface import implements

# CMF
from Products.CMFCore import permissions as CCP

# Archetypes imports
from Products.Archetypes.public import StringField, StringWidget, registerType,\
     Schema, ReferenceField, ComputedField, ComputedWidget

# Products imports
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget

from Products.ATContentTypes.interface import IATLink, IATContentType

from Products.PloneArticle.proxy import BaseInnerContentProxy, \
    BaseInnerContentProxySchema
from Products.PloneArticle.interfaces import ILinkInnerContentProxy

# Defines schema
LinkInnerContentProxySchema = BaseInnerContentProxySchema.copy() + Schema((
    ComputedField(
        'remoteUrl',
        primary=True,
        expression="""context.getPrimaryValue('')""",
        widget=ComputedWidget(
            label='Remote url',
            label_msgid='label_remote_url',
            i18n_domain='plonearticle',
            ),
        ),
    ReferenceField(
        'referencedContent',
        relationship='article_link',
        widget=ReferenceBrowserWidget(
            label='Referenced link',
            label_msgid='label_referenced_link',
            i18n_domain='plonearticle',
            ),
        ),
    StringField(
        'attachedLink',
        widget=StringWidget(
            label='Link',
            label_msgid='label_link',
            i18n_domain='plonearticle',
            ),
        ),
    ))

class LinkInnerContentProxy(BaseInnerContentProxy):
    """Proxy implementing IATLink. It means this proxy has a remoteUrl
    method.

    remoteUrl returns attached link by default if existing otherwise returns
    the referenced content.
    """

    implements(ILinkInnerContentProxy)
    security = ClassSecurityInfo()

    schema = LinkInnerContentProxySchema

    # You can only reference content implementing IATLink interface
    referenceable_interfaces = (IATContentType,)

    security.declareProtected(CCP.View, 'getPrimaryValue')
    def getPrimaryValue(self, default=None):
        """getPrimaryValue proxy method for links
        Returns referenced absolute url or attached link.
        Attached link has priority on referenced url.
        """

        # If an attached link is defined return its value
        field = self.getField('attachedLink')
        if field.get_size(self) > 0:
            accessor = field.getAccessor(self)
            return accessor()

        # Attached field is empty. Use referenced content
        referenced_content = self.getReferencedContent()
        if referenced_content is not None:
            return referenced_content.absolute_url()

        return default

    security.declareProtected(CCP.View, 'SearchableText')
    def SearchableText(self):
        """indexing links is useless
        """
        return self.Title() + self.Description()

    security.declareProtected(CCP.View, 'getLinkIcon')
    def getLinkIcon(self):
        """return link_icon or referenced conten icon
        """
        attachField = self.getField('attachedLink')
        if attachField.get_size(self) > 0 :
            return 'link_icon.gif'
        elif self.getReferencedContent() is not None :
            return self.getReferencedContent().getIcon(True)    
        return self.getIcon(True)    



registerType(LinkInnerContentProxy)
