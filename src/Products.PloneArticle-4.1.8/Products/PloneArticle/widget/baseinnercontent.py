# -*- coding: utf-8 -*-
## Defines BaseInnerContentWidget
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
Defines BaseInnerContentWidget
"""

__docformat__ = 'restructuredtext'

from time import strftime

# Zope imports
from AccessControl import ClassSecurityInfo
from OFS.Image import File

# Archetypes imports
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.Widget import TypesWidget

_marker = []

class BaseInnerContentWidget(TypesWidget):
    """"""

    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro' : "pa_baseinnercontentwidget",
        'new_content_macro': "pa_baseinnercontentwidget",
        })

    security = ClassSecurityInfo()

    security.declarePublic('process_form')
    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False):
        """
        Calls process_form on all sub fields.

        Like all process_form methods, returns a tuple and a dictionary
        inside a tuple.

        The tuple contains all results of calling process_form on sub fields
        of inner content:

        ({'description': ('', {}),
          'id': ('imageinnercontentproxy.2007-01-30.8023847640', {}),
          'title': ('', {})})
        """

        # Get form keys and just keep those related to the field
        # Key : <field id>_<sub field id>_<sub field index>
        form_keys = form.keys()
        # field_name can be for example "images"
        field_name = field.getName()
        # key_prefix can be for example "images_innercontent"
        key_prefix = '%s_innercontent' % field_name
        # position_key can be for example "images_innercontent_position"
        position_key = '%s_position' % key_prefix
        key_prefix_length = len(key_prefix)
        field_keys = [k for k in form_keys if k.startswith(key_prefix) and k not in (position_key,)]

        # The filtered field_keys can be for example:
        # ['images_innercontent160231_tempFileIndex',
        #  'images_innercontent160231_isTemporary',
        #  'images_innercontent160231_id',
        #  'images_innercontent160231_description',
        #  'images_innercontent160231_title']

        # Group all results in form by inner content widget.
        sub_forms = {}
        for field_key in field_keys:
            # Get sub field index
            sub_field_index = field_key[key_prefix_length:(key_prefix_length+6)]
            sub_field_name = field_key[(key_prefix_length+7):]
            if not sub_forms.has_key(sub_field_index):
                sub_forms[sub_field_index] = {}

            sub_forms[sub_field_index][sub_field_name] = form.get(field_key)

        # The resulting subforms dictionary may look like this:
        # {'160231': {'tempFileIndex': 0,
        #             'description': '',
        #             'id': 'imageinnercontentproxy.2007-01-30.3505314205',
        #             'isTemporary': 1,
        #             'title': ''}}

        # Sort sub forms py position
        inner_content_position = form.get(position_key, [])

        # The inner_content_position may look like this:
        # ['160231']

        sub_forms = [sub_forms[k] for k in inner_content_position]

        # The sub_forms may look like this now:
        # [{'tempFileIndex': 0,
        #   'description': '',
        #   'id': 'imageinnercontentproxy.2007-01-30.3505314205',
        #   'isTemporary': 1,
        #   'title': ''}]

        inner_content_schema = field.getInnerContentSchema(instance)
        inner_content_fields = inner_content_schema.fields()
        # inner_content_fields may look like this now:
        # [<Field id(string:rw)>,
        #  <Field title(string:rw)>,
        #  <Field description(text:rw)>,
        #  <Field referencedContent(reference:rw)>,
        #  <Field image(computed:r)>,
        #  <Field attachedImage(image:rw)>]

        value = []

        request = instance.REQUEST

        for sub_form in sub_forms:
            inner_content_values = {}
            for inner_content_field in inner_content_fields:
                widget = inner_content_field.widget
                inner_content_value = widget.process_form(instance, inner_content_field, sub_form, empty_marker=_marker)
                if inner_content_value is _marker or inner_content_value is None:
                    continue
                inner_content_values[inner_content_field.getName()] = inner_content_value
            value.append(inner_content_values)

        return tuple(value), {}

    security.declarePublic('makeWidgetId')
    def makeWidgetId(self, fieldName, widget_index):
        """
        """
        return '%s-innercontent%06d' % (fieldName, widget_index)

    security.declarePublic('makeInnerContentWidgetId')
    def makeInnerContentWidgetId(self, fieldName, index, icf_name):
        """
        Return an id for a proxy field name

        @param fieldName: InnerContentField name
        @param index: proxy content index
        @param icf_name: proxy field name
        """
        return '%s_innercontent%06d_%s' % (fieldName, index, icf_name)

    security.declarePublic('innerContentWidget')
    def innerContentWidget(self, field_name, index, inner_content,
                           inner_content_field, mode='edit'):
        """
        """
        icf_name = inner_content_field.getName()
        widget_field_name = self.makeInnerContentWidgetId(field_name, index,
                                                          icf_name)

        return inner_content.widget(widget_field_name,
                                    field=inner_content_field,
                                    mode=mode)

    security.declarePublic('generateWidgetIndex')
    def generateWidgetIndex(self):
        """
        """
        # we use hour-minutes-seconds as a unique number
        # should be valid for an editing round within the same form!
        return int(strftime("%H%M%S"))

registerWidget(BaseInnerContentWidget,
               title='BaseInnerContent',
               description=(''),
               used_for=('Products.PloneArticle.field.BaseInnerContentWidget',)
               )
