# -*- coding: utf-8 -*-
## Defines BaseInnerContentField
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
Defines BaseInnerContentProxy and BaseFileContentProxy
"""

__docformat__ = 'restructuredtext'

# Zope imports
from zope.interface import implements
from zope.component import queryUtility

import transaction
from AccessControl import ClassSecurityInfo

# CMF
from Products.CMFCore import permissions as CCP
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.atapi import BaseContentMixin
from Products.Archetypes.atapi import MinimalSchema
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import ReferenceField
from Products.Archetypes.atapi import TextField
from Products.Archetypes.config import UUID_ATTR
from Products.Archetypes.utils import shasattr

from plone.i18n.normalizer.interfaces import IUserPreferredURLNormalizer
from plone.i18n.normalizer.interfaces import IURLNormalizer

# Other imports
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget
from Products.Archetypes.Widget import TextAreaWidget

from Products.PloneArticle.config import PLONEARTICLE_TOOL
from Products.PloneArticle.interfaces import IBaseInnerContentProxy

# No need to have all dublin core metadata
BaseInnerContentProxySchema = MinimalSchema.copy() + Schema((
    TextField(
        'description',
        searchable=True,
        default='',
        accessor="Description",
        widget=TextAreaWidget(
            label='Description',
            description="A short summary of the content",
            label_msgid="label_description",
            description_msgid="help_description",
            i18n_domain="plone"),
        ),
    ReferenceField(
        'referencedContent',
        relationship='article_proxy',
        allowed_types_method='getReferenceablePortalTypes',
        keepReferencesOnCopy=True,
        widget=ReferenceBrowserWidget(
            label='Referenced content',
            label_msgid='label_referenced_content',
            i18n_domain='plonearticle',
            ),
        ),
))

class BaseInnerContentProxy(BaseContentMixin):
    """This is a proxy between article and a referenced content.

    A referenced content can be defined outside the article and a proxy is just
    a placeholder for this external object or internal object.

    A proxy is a traversable content so it can be accessed from its url.
    """

    implements(IBaseInnerContentProxy)
    security = ClassSecurityInfo()

    schema = BaseInnerContentProxySchema
    meta_type = 'BaseInnerContentProxy'
    archetype_name = 'Base Content Inner Proxy'
    typeDescription= ''
    typeDescMsgId  = ''
    global_allow = False
    _at_rename_after_creation = True

    # subclasses *must* define this attribute. see getReferencedContentInterfaces
    # referenceable_interfaces = ()

    def __setattr__(self, key, value):
        # Patch this method to get the original uid of source object
        if key == UUID_ATTR and value is None:
            if not shasattr(self, '_v_src_uid'):
                self._v_src_uid = getattr(self, UUID_ATTR, None)

        BaseContentMixin.__setattr__(self, key, value)

    security.declareProtected(CCP.View, 'getAttachedContentField')
    def getAttachedContentField(self):
        """
        Return the field marked has 'attached_content'
        """
        schema = self.Schema()
        fields = schema.filterFields(attached_content=True)
        if len(fields) > 0:
            return fields[0]
        return None

    security.declareProtected(CCP.View, 'getPrimaryValue')
    def getPrimaryValue(self, referenced_fieldname, attached_fieldname,
                        default=None):
        """Returns value of referenced field or attached field.

        Attached field has priority on referenced field.
        @param referenced_fieldname: field we want to check in the referenced
        content.
        @param attached_fieldname: attached field of the inner proxy
        @param default: Defautl value if referenced and attached field are empty
        """

        # If an attached field is defined return its value
        field = self.getField(attached_fieldname)
        if field.get_size(self) > 0:
            accessor = field.getAccessor(self)
            return accessor()

        # Attached field is empty. Use referenced content
        referenced_content = self.getReferencedContent()
        if referenced_content is not None:
            field = referenced_content.getField(referenced_fieldname)
            if field is not None and field.get_size(referenced_content) > 0:
                accessor = field.getAccessor(referenced_content)
                return accessor()

        return default

    def getReferenceableInterfaces(klass,):
        """
        Returns tuple of interfaces that a content class must provide so that
        the proxy can reference it. Usually the proxy will also provide this
        interface.

        A proxy class must have an attribute 'referenced_content_interfaces'
        that is a tuple of interfaces.
        """
        return klass.referenceable_interfaces
    getReferenceableInterfaces = classmethod(getReferenceableInterfaces)

    security.declareProtected(CCP.View, 'getReferenceablePortalTypes')
    def getReferenceablePortalTypes(self, field):
        """
        Returns a tuple of portal types that this proxy can reference, for
        the particular portal_type using this proxy (i.e, PloneArticle.images
        types can be different from PloneArticleLike.images)
        """
        pat = getToolByName(self, PLONEARTICLE_TOOL)
        return pat.getReferenceablePortalTypesFor(self, field)

    security.declareProtected(CCP.View, 'SearchableText')
    def SearchableText(self):
        """
        Returns string used by SearchableText index.
        Use BaseObject SearchableText method and add referencedContent
        SearchableText value
        """

        # Get default SearchableText
        value = BaseContentMixin.SearchableText(self)

        # Get referenced content
        content = self.getReferencedContent()

        if content is None:
            return value

        # Add referenced content Searchable text
        try:
            value += ' ' + content.SearchableText()
        except AttributeError:
            pass
        return value


def innerContentAdded(ob, event):
    """Supersedes the BaseInnerContentProxy.manage_afterAdd with events machinery,
    see events.zcml"""

    item = event.object
    container = event.newParent
    # FIXME: Uuuuugly, but required by Archetypes that has no events machinery
    super(ob.__class__, ob).manage_afterAdd(item, container)

    # Get source object UID
    is_copy = getattr(item, '_v_is_cp', None)
    src_uid = getattr(ob, '_v_src_uid', None)

    if is_copy and src_uid is not None:
        # Get source object
        atool = getToolByName(ob, "archetype_tool")
        src_obj = atool.getObject(src_uid)

        if src_obj is not None:
            # Get references from source object
            refs = src_obj.getReferenceImpl()

            # Copy references from source object to new created object
            for ref in refs:
                ob.addReference(ref.getTargetObject(), relationship=ref.relationship)

    return


class BaseFileContentProxy(BaseInnerContentProxy):
    """
    Rename content id according to attached file name
    """
    security = ClassSecurityInfo()
    _at_rename_after_creation = False


    security.declarePrivate('renameFromFileName')
    def renameFromFileName(self, field=None):
        """
        field must be a FileField or derivative. If field is None, we use
        getAttachedContentField.
        """
        if field is None:
            field = self.getAttachedContentField()

        filename = field.getFilename(self)

        if not filename:
            return

        if not isinstance(filename, unicode):
            charset = self.getCharset()
            filename = unicode(filename, charset)

        request = getattr(self, 'REQUEST', None)
        if request is not None:
            normalize = IUserPreferredURLNormalizer(request).normalize
        else:
            normalize = queryUtility(IURLNormalizer).normalize

        clean_filename = normalize(filename)

        self_id = self.getId()
        if clean_filename != self_id:
            # new id to be set
            invalid_id = True
            check_id = getattr(self, 'check_id', None)

            if check_id is not None:
                invalid_id = check_id(clean_filename, required=1)

            if invalid_id:
                parent_ids = self.getParentNode().objectIds()
                base_name = clean_filename
                extension = ''
                dot_pos = clean_filename.rfind('.')
                if dot_pos > 0:
                    base = clean_filename[:dot_pos]
                    extension = clean_filename[dot_pos:]

                idx = 0
                while clean_filename in parent_ids \
                          and clean_filename != self_id:
                    idx += 1
                    clean_filename = "%s-%d%s" % (base, idx, extension)

            if clean_filename == self_id:
                # we have recomputed the same numbered file name. Do nothing
                return

            # got a clean file name - rename it
            # apply subtransaction. w/o a subtransaction renaming
            # fails when the type is created using portal_factory
            transaction.savepoint(optimistic=True)
            self.setId(clean_filename)
            self.reindexObject()

