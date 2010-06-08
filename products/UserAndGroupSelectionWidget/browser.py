# -*- coding: utf-8 -*-
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

__author__ = """Robert Niederreiter <robertn@bluedynamics.com>"""
__docformat__ = 'plaintext'

import types

from zope.interface import implements
from Products.Five import BrowserView

from Products.PlonePAS.interfaces.group import IGroupIntrospection

from ZTUtils import make_query
from Products.CMFCore.utils import getToolByName

from interfaces import IUserAndGroupSelectView
from interfaces import IUserAndGroupSelectPopupView

from memberlookup import MemberLookup
from alphabatch import AlphaBatch


class UserAndGroupSelectView(BrowserView):
    """See interfaces.IUserAndGroupSelectView for documentation details.
    """
    
    def getUserOrGroupTitle(self, id):
        pas = getToolByName(self.context, 'acl_users')
        user = pas.getUserById(id)
        
        if user is not None:
            fullname = self._getPropertyForMember(user, 'fullname')
            return fullname or id
        
        for pluginid, plugin in pas.plugins.listPlugins(IGroupIntrospection):
            group = plugin.getGroupById(id)
            if group is not None:
                title = self._getPropertyForMember(group, 'title')
                return title or id
        
        return id
    
    def _getPropertyForMember(self, member, propertyname):
        propsheets = member.listPropertysheets()
        for propsheettitle in propsheets:
            propsheet = member.getPropertysheet(propsheettitle)
            property = propsheet.getProperty(propertyname, None)
            if property:
                return property
        
        return None


class UserAndGroupSelectPopupView(BrowserView):
    """See interfaces.IUserAndGroupSelectPopupView for documentation details.
    """
    
    implements(IUserAndGroupSelectView)
    
    def initialize(self):
        """Initialize the view class.
        """
        schema = self.context.Schema()
        fieldId = self.request['fieldId']
        
        # compoundfield and arrayfield compatibility
        field = self.context
        fieldIds = fieldId.split('-')
        for fieldId in fieldIds:
            field = field.schema.get(fieldId)
        
        self.multivalued = field.multiValued
        self.widget = field.widget
        self.memberlookup = MemberLookup(self.context,
                                         self.request,
                                         self.widget)
        
    def getObjectUrl(self):
        r = '%s/%s' % (self.context.absolute_url(), 'userandgroupselect_popup')
        return r
        
    def getQueryUrl(self, **kwargs):
        baseUrl = self.context.absolute_url()
        if self.request.get('fieldId', '') != '':
            baseUrl += '/userandgroupselect_popup'
        query = self._getQueryString(**kwargs)
        url = '%s?%s' % (baseUrl, query)
        return url
    
    def isSelected(self, param, value):
        param = self.request.get(param)
        if param:
            if param is types.StringType:
                param = [param]
            if value in param:
                return True
        return False
    
    def getGroupsForPulldown(self):
        ret = [('ignore', '-')]
        return ret + self.memberlookup.getGroups()
    
    def getBatch(self):
        members = self.memberlookup.getMembers()
        return AlphaBatch(members, self.context, self.request)
    
    def usersOnly(self):
        return self.widget.usersOnly
    
    def groupsOnly(self):
        return self.widget.groupsOnly
    
    def multiValued(self):
        if self.multivalued:
            return 1
        return 0
    
    def _getQueryString(self, **kwargs):
        params = dict()
        for key in self.request.form.keys():
            params[key] = self.request.form[key]
        params.update(kwargs)
        query = make_query(params) 
        return query