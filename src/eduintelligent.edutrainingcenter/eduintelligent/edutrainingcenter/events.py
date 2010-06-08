# -*- coding: utf-8 -*-
#
# File: eduTrainingCenter/events.py
#
# Copyright (c) 2007 Erik Rivera Morales <erik@ro75.com>
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

"""
$Id$
"""

__author__ = """Erik Rivera Morales <erik@iservices.com.mx>"""
__docformat__ = 'plaintext'
__licence__ = 'GPL'

from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from eduintelligent.edutrainingcenter.interfaces import IEduMember, ITrainingCenter

def verifyGroups(obj, event):
    """
    Consolidation for all the groups that the user belogs to
    """
    print "Modify %s on %s" % (obj.getPhysicalPath(), event)
    #IEduMember(obj).verifyGroups()

    context = IEduMember(obj)
    tctool = getToolByName(context, 'portal_tctool')
    parent = context.aq_inner.aq_parent
    parent = parent.getGroupId()
    user_groups = context.getGroups()
    
    dinamic_grps = [x for x in user_groups if x.startswith(parent+'_group')]
    static_grps = []
    
    #First, Make a list with all the static groups
    #company_division
    #Is a MultiSelectionWidget. Returns a list
    company_division = context.getCompany_division()
    if company_division:
        static_grps.extend(company_division)

    #company_work_area
    #It is a SelectionWidget. It always returns an string
    company_work_area = context.getCompany_work_area()
    if company_work_area:
        static_grps.append(company_work_area)
    
    #company_position
    #It is a SelectionWidget. It always returns an string
    company_position = context.getCompany_position()
    if company_position:
        static_grps.append(company_position)
    
    #Join all dynamic and static groups along with the
    #corresponding training center group.
    
    new_grps=[parent,] # add user to training center group
    new_grps.extend(dinamic_grps)
    new_grps.extend(static_grps)

    user_groups = frozenset(user_groups)
    new_grps = frozenset(new_grps)
    remove = user_groups - new_grps
    final = (user_groups | new_grps) - remove
    if remove:
        print "\nRemove from EduMember",list(remove)
        tctool.removeGroupUser(user=context.getId(),groups=list(remove))

    tctool.addGroupUser(user=context.getId(),groups=list(final))
    
    ########### assign the main group ######   
    main_group = context.getMain_group()
    if not main_group:
        context.setMain_group(parent)
    
def definePermissions(obj, event):
    """
    """
    #nota: see if is necesary when edit the training center, may be, the UserFiel modify the localroles
    context = ITrainingCenter(obj)
    group = context.getGroupId()
    context.manage_setLocalRoles(group, ['Member',])
    context.reindexObjectSecurity()
    
