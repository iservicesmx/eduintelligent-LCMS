# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 by BlueDynamics Alliance, Austria
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
Phil Auersperg <phil@bluedynamics.com>"""
__docformat__ = 'plaintext' 

import types
from Acquisition import aq_base

def takeRoleFromAllCurrentSet(obj, role, reindex=1, recursive=0):
    """Take all from all current on obj set local roles the given role."""
    userids = obj.users_with_local_role(role)
    for uid in userids:
        currentroles = obj.get_local_roles_for_userid(userid=uid)
        filteredroles = [cur for cur in currentroles if cur != role]
        print "delete local roles for %s" % uid ,
        obj.manage_delLocalRoles([uid])
        if filteredroles:                
            print "but preserve roles %s" % filteredroles
            obj.manage_setLocalRoles(uid, filteredroles)
    # if recursive: handle subobjects
    if recursive and hasattr( aq_base(obj), 'contentValues' ):
        for subobj in obj.contentValues():
            takeRoleFromAllCurrentSet(subobj, role, 0, 1)
    if reindex:
        # reindexObjectSecurity is always recursive
        obj.reindexObjectSecurity()

def setLocalRoles(instance, userids, roles=[], cumulative=False):
    """Sets local roles on instance."""
    if not roles: 
        return
    if type(roles) not in (types.ListType, types.TupleType):
        roles = [roles]
    if not cumulative:
        for role in roles:
            takeRoleFromAllCurrentSet(instance, role, reindex=0)
    for uid in userids:
        print ": add local roles %s for users %s" % (roles, uid)
        instance.manage_addLocalRoles(uid, roles)
        
    # It is assumed that all objects have the method
    # reindexObjectSecurity, which is in CMFCatalogAware and
    # thus PortalContent and PortalFolder.
    instance.reindexObjectSecurity()
            
