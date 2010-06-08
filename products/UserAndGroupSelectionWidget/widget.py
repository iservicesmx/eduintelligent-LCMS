# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 by BlueDynamics Alliance, Austria
#
# initially this code was derived from ATMemberselectWidget
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """Jens Klein <jens@bluedynamics.com>,
                Robert Niederreiter <robertn@bluedynamcis.com>"""
__docformat__ = 'plaintext' 

import types
from zope.component import ComponentLookupError
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.utils import shasattr
from interfaces import IGenericGroupTranslation

class UserAndGroupSelectionWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro'                 : "userandgroupselect",
        'helper_js'             : ('userandgroupselect.js',),
        'size'                  : 7,    # size of form-element taking the users
        'groupName'             : '',    # takes the given group as default, a group id
        'usersOnly'             : False, # only allow user selection
        'groupsOnly'            : False, # allow only group selection
        'groupIdFilter'         : '*',   # allow all groups
        })

    security = ClassSecurityInfo()    

    security.declarePublic('process_form')
    def process_form(self, instance, field, form, empty_marker=None, emptyReturnsMarker=None,):
        """process the form data and return it."""
        result = TypesWidget.process_form (self, instance, field, form, 
                                           empty_marker, emptyReturnsMarker, )
        if result is empty_marker:
            return result
        value, kwargs = result
        
        # The widget always returns a empty item (strange) when we use the multival option.
        # Remove the empty items manually
        if type(value) is types.ListType:
            value = [item for item in value if item]
        return value, kwargs
    
    security.declarePublic('getGroupId')
    def getGroupId(self, instance):
        groupid = self.groupName
        try:
            translator = IGenericGroupTranslation(instance)
        except ComponentLookupError:
            pass
        except TypeError, e:
            if e[0] == 'Could not adapt':
                pass
            else:
                raise        
        else:
            groupid = translator.translateToRealGroupId(self.groupName)
        return groupid
            

registerWidget(UserAndGroupSelectionWidget,
               title='User and Group Selection Widget',
               description=('You can select users searched from a popup window.'),
               used_for=('Products.Archetypes.Field.LinesField',
	                     'Products.Archetypes.Field.StringField', )
               )
