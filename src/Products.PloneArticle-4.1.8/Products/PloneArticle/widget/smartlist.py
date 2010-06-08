# -*- coding: utf-8 -*-
## Widget for SmartListField
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
Widget for SmartListField
"""

__docformat__ = 'restructuredtext'

# Zope imports
from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.Widget import TypesWidget

class SmartListWidget(TypesWidget):
    """"""
    
    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro' : "pa_smartlistwidget",
        })

    security = ClassSecurityInfo()

    security.declarePublic('getSelectablePortalTypes')
    def getSearchablePortalTypes(self, field, instance):
        """
        Return a Display list for searchable portal_types
        """
        
        pt = getToolByName(instance, 'portal_types')
        allowed_types = field.getAllowedTypes(instance)
        typesList = [pt.getTypeInfo(t) for t in allowed_types]
        
        return instance.createMultiColumnList(typesList, numCols=2,
                                              sort_on='title_or_id')
        
    security.declarePublic('getSelectedTypes')
    def getSelectedTypes(self, search_criterias):
        """
        """
        return search_criterias.get('portal_type', ())

    security.declarePublic('getVisitedUIDs')
    def getVisitedUIDs(self, excluded_uids, referenced_uids):
        """
        """
        visited_uids = dict.fromkeys(referenced_uids)
        visited_uids.update(excluded_uids)
        return visited_uids

    security.declarePublic('getAddableCriterias')
    def getAddableCriterias(self, field, instance, search_criterias):
        """
        """
        return [idx for idx in field.getAllowedCriterias(instance)
                if idx not in ('SearchableText', 'portal_type',)]

    security.declarePublic('getAddedCriterias')
    def getAddedCriterias(self, search_criterias):
        """
        """
        return [idx for idx in search_criterias.keys()
                if idx not in ('SearchableText', 'portal_type',)]
    
    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False):
        """
        collect form values into a dictionnary suitable for field
        """

        fieldName = field.getName()
        value = form.get(fieldName + '_ref_uids', [])
        
        kwargs = {}

        # form record are not dictionnaries, we must create a real one
        kwargs['search_criterias'] = {}
        kwargs['search_criterias'].update(
            form.get(fieldName + '_search_criterias', {})
            )

        kwargs['uids_found'] = form.get(fieldName + '_uids_found', [])
        kwargs['auto_reference'] = form.get(fieldName + '_auto_reference',
                                            False)

        return value, kwargs
            
    
registerWidget(SmartListWidget,
               title='SmartList',
               description=(''),
               used_for=('Products.PloneArticle.field.smartlistfield.SmartListField',)
               )
