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
Defines BaseInnerContentField
$Id: baseinnercontent.py 8575 2008-06-23 15:13:26Z encolpe $
"""

__docformat__ = 'restructuredtext'

# Python imports
from types import ListType, TupleType, DictType
from itertools import izip, count

# Zope imports
from Acquisition import aq_base
from AccessControl import ClassSecurityInfo, getSecurityManager
from ZODB.POSException import ReadConflictError
from zope.interface import implements

# CMF imports
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.Registry import registerField
from Products.Archetypes.Field import Field
from Products.Archetypes.utils import shasattr

# Products imports
from Products.PloneArticle.field import InnerContentContainer
from Products.PloneArticle.interfaces import IBaseInnerContentField, \
    IBaseInnerContentProxy

class BaseInnerContentField(Field):
    """An inner content field contains inner content objects

    Inner content objects are stored in a folderish sub object of instance
    """

    implements(IBaseInnerContentField)

    _properties = Field._properties.copy()
    _properties.update({
        'type' : 'object',
        'inner_portal_type' : 'BaseInnerContent',
        'default': (),
        'default_content_type': None,
        })

    security  = ClassSecurityInfo()

    getContainerName = Field.getName

    security.declarePrivate('get')
    def get(self, instance, **kwargs):
        """Classical Field API. Specific keyword args (kwargs):
        * mimetype: If "text/plain", returns the indexable text"
        * filtered: if True, provides only the objects the user can view
        """
        # If mimetype is text/plain returns indexable value
        mimetype = kwargs.get("mimetype", None)

        if mimetype == "text/plain":
            return self.getIndexableValue(instance)

        # Returns a list of inner content objects
        name = self.getContainerName()
        try:
            container = instance._getOb(name)
        except ReadConflictError:
            raise
        except Exception, msg:
            return ()

        if isinstance(container, InnerContentContainer):
            filtered = kwargs.get('filtered', False)
            subitems = container.objectValues()
            if filtered:
                out = []
                sm = getSecurityManager()
                for item in subitems:
                    referenced = item.getReferencedContent()
                    if referenced is not None:
                        # External item
                        if sm.checkPermission('View', referenced):
                            out.append(item)
                    else:
                        # Embedded item
                        out.append(item)
                return out
            return subitems
        return ()

    # LinguaPlone needs this, as it thinks it always deals with ObjectField...
    security.declarePrivate('getRaw')
    def getRaw(self, instance, **kwargs):
        return self.get(instance, **kwargs)

    security.declarePrivate('get_size')
    def get_size(self, instance, **kwargs):
        """Sum of all inner content objects size"""
        objs = self.get(instance, **kwargs)
        size = 0
        for obj in objs:
            size += obj.get_size()
        return size

    security.declarePublic('getContentType')
    def getContentType(self, instance, fromBaseUnit=True):
        """ return MIME type """
        f = self.get(instance)
        return getattr(f, 'content_type', self.default_content_type)

    security.declarePrivate('set')
    def set(self, instance, value, **kwargs):
        """
            Set inner fields of this field.

            self is an instance of BaseInnerContentField instance is the
            instance of the article we are working on.

            value can be:
                InnerContentContainer
                A list of InnerContentProxy objects:
                A list of dictionaries: Each item of the dictionary will be handled

            kwargs are optionnals arguments changing the way this field is
            updated :
                "update": If True, update inner content proxies present in the value's dict list.
                          If False, update inner content proxies present in the value's dict list,
                          but delete all inner content proxies that are missing from the list but
                          have been created before.
                "_initializing_": creates a new inner container

            This method calls the mutator of each inner field of this field, by
            sending to it only what has been returned by the associated widget.

            Example of the value when the image already existed and hasn't changed:

            ({'description': ('Existing image', {}),
              'id': ('imageinnercontentproxy.2007-01-30.0017453092', {}),
              'title': ('Existing image', {})},)

            Example of value when there is a new image:

            ({'description': ('New image', {}),
              'id': ('imageinnercontentproxy.2007-02-04.7516632708', {}),
              'attachedImage': (<BaseUnit at fss.JPG>, {}),
              'title': ('New image', {})})

            ({'description': ('Referenced image', {}),
              'referencedContent': ('817b168ec61fbfcb080de02629431631', {}),
              'id': ('imageinnercontentproxy.2007-02-04.1880613482', {}),
              'title': ('Referenced image', {})})

        """

        if kwargs.get('_initializing_', False):
            return

        if isinstance(value, InnerContentContainer):
            return self.set(instance, value.objectValues(), **kwargs)

        # value must be a list of dictionnary
        # Each dictionnary defines values of inner content fields
        # Values can be wrapped into a tuple if for example you want to
        # define some extra args on the field mutator
        if type(value) not in (ListType, TupleType,):
            raise ValueError, \
                  "Value must be a list or a tuple, get: %s" % type(value)

        # Value can be a list of dictionnary or a list of InnerContent proxy
        # objects. In this case, wrap object into a dictionnary
        for index in range(0, len(value)):
            item = value[index]

            if IBaseInnerContentProxy.providedBy(item):
                schema = item.Schema()
                data = {}

                # Loop on fields and extract data using accessor
                for field in schema.fields():
                    if 'w' not in field.mode:
                        continue

                    field_id = field.getName()
                    accessor = field.getAccessor(item)

                    if accessor is None:
                        continue

                    data[field_id] = accessor()

                value[index] = data

        # Get inner container
        container_name = self.getContainerName()
        if shasattr(instance, container_name):
            container = getattr(instance, container_name, None)
        else:
            container = None

        # Do nothing if value is empty and container doesn't already exist
        if not isinstance(container, InnerContentContainer) and not value:
            return

        # Create a new container if it doesn't already exist
        if not isinstance(container, InnerContentContainer):
            container = InnerContentContainer(container_name)
            instance._setObject(container_name, container)
            container = instance._getOb(container_name)
            container.initializeArchetype()
            #instance._p_changed = 1

        # 'update' argument is a switch for innercontent deletion:
        # - if True, ids that are not present in the request WON'T be destroyed
        # - if False or doesn't exist, all ids that are not in request WILL be deleted.
        update = kwargs.get('update', False)

        # Format all field values to be a tuple. If no extra args defined,
        # replace by an empty dictionnary
        for item in value:
            for item_key in item.keys():
                item_value = item[item_key]

                if type(item_value) not in (TupleType, ListType,):
                    item[item_key] = (item_value, {})

        # Build a list containing all inner content ids to be replaced or updated
        inner_content_ids = [x['id'][0] for x in value]

        # If update not in kwargs, delete objects in container
        if not update and container is not None:
            inner_content_ids_to_remove = [x for x in container.objectIds()
                                           if x not in inner_content_ids]
            container.manage_delObjects(ids=inner_content_ids_to_remove)

        # Check for new inner contents
        for item, item_index in izip(value, count()):
            inner_content_field_values = item.copy()
            inner_content_id = inner_content_field_values['id'][0]
            # no need to reindex until a new inner content is really added
            to_reindex = False
            # Create a new inner content if it doesn't exist
            if not shasattr(container, inner_content_id):
                container.invokeFactory(type_name=self.inner_portal_type,
                                        id=inner_content_id)
                to_reindex = True

            # reorder content only if update not in kwargs
            if not update:
                content_position = container.getObjectPosition(inner_content_id)
                if content_position != item_index:
                    container.moveObjectToPosition(inner_content_id, item_index)

            inner_content = getattr(container, inner_content_id)
            # removing id from field_values since id shouldn't be updated
            # (it's the key)
            del inner_content_field_values['id']

            # Update inner content fields (new and already existing)
            for field_name, field_args in inner_content_field_values.items():
                field = inner_content.getField(field_name)
                mutator = field.getMutator(inner_content)
                mutator(field_args[0], **field_args[1])
                to_reindex = True

            # Then reindex object
            if to_reindex:
                inner_content.reindexObject()

    security.declarePublic('getInnerContentSchema')
    def getInnerContentSchema(self, instance):
        """Returns a inner content schema."""

        atool = getToolByName(instance, 'archetype_tool')
        registered_schemas = [x['schema'] for x in atool.listRegisteredTypes()
                              if x['portal_type'] == self.inner_portal_type]
        schema = registered_schemas[0]
        return schema

    security.declarePublic('getInnerContentAttachedField')
    def getInnerContentAttachedField(self, instance):
        """Return the field instance responsible of holding an attached file, or
        None if no field is defined for this.
        """
        schema = self.getInnerContentSchema(instance)
        fields = schema.filterFields(attached_content=True)
        count = len(fields)
        if count == 0:
            return None
        if count == 1:
            return fields[0]

        raise (AssertionError,
               "%d fields are defined as holder for attached content for %s "
               "field: %s" % (count, instance.portal_type, self.getName()))

    security.declarePublic('getTemporaryInnerContent')
    def getTemporaryInnerContent(self, instance):
        """Returns a temporary inner content"""

        atool = getToolByName(instance, "archetype_tool")
        types = atool.listRegisteredTypes()
        types = [t for t in types if t['portal_type'] == self.inner_portal_type]

        # Inner Content is not registered
        if not types:
            raise ValueError, "Inner content is not registered: %s" % \
                self.inner_portal_type

        # Create temporary inner content
        inner_klass = types[0]['klass']
        inner_content_id = instance.generateUniqueId(self.inner_portal_type)
        inner_content = inner_klass(inner_content_id)
        inner_content._at_is_fake_instance = True
        inner_content._is_fake_instance = True
        wrapped = inner_content.__of__(instance)
        wrapped.initializeArchetype()
        return wrapped

    security.declarePrivate('getIndexableValue')
    def getIndexableValue(self, instance):
        """
        Returns string value used on SearchableText index
        """

        proxies = self.get(instance)
        return " ".join([x.SearchableText() for x in proxies])

    security.declarePublic('writeable')
    def writeable(self, instance, debug=False):
        """Overriding standard Field.writeable such this field is not writeable
        on temporary objects (using portal_factory)"""

        if instance.isTemporary():
            return False
        return super(BaseInnerContentField, self).writeable(instance, debug)


registerField(BaseInnerContentField,
              title='BaseInnerContent',
              description=('Used to store objects implementing IBaseInnerContent.')
             )
