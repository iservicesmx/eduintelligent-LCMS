# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 by Erik Rivera Morales <erik@ro75.com>
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

__author__ = """Erik Rivera Morales <erik@ro75.com>"""
__docformat__ = 'plaintext'

import os
import csv
from cStringIO import StringIO

import transaction
from zope.interface import implements
from zope.component import getUtility
from zope.event import notify

from Acquisition import aq_inner, aq_parent
from plone.i18n.normalizer.interfaces import IIDNormalizer
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName


from interfaces import ITCTool
from Products.CMFCore.utils import UniqueObject
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.Archetypes.atapi import *
from Products.Archetypes.interfaces import IObjectInitializedEvent
from Products.Archetypes.event import ObjectInitializedEvent


from eduintelligent.edutrainingcenter.config import PROJECTNAME, PATH_IMPORT
from eduintelligent.edutrainingcenter import logger


schema = Schema((
    LinesField(
        name='config1',
        widget=LinesField._properties['widget'](
            label='Configuration1',
            label_msgid='tc_label_config1',
            i18n_domain='trainingcenter',
        )
    ),

),
)


TCTool_schema = BaseSchema.copy() + \
    schema.copy()


class TCTool(UniqueObject, BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(ITCTool)
    meta_type = 'TCTool'
    _at_rename_after_creation = True

    schema = TCTool_schema

    def __init__(self, id=None):
        BaseContent.__init__(self,'portal_tctool')
        self.setTitle('')


    def at_post_edit_script(self):
        self.unindexObject()
        
    # Methods
    security.declarePublic('addGroup')
    def addGroup(self, parent='', prefix='', name='', description=''):
        """
        add a group from parent
        """
        #print "addGroups"
        #print "name: ",name
        group_id = parent + '_' + prefix +'_' + name.replace(' ','-')
        util = getUtility(IIDNormalizer)
        group_id = util.normalize(unicode(name,'utf-8'))
        group_id = parent + '_' + prefix +'_' + group_id
        grouptool = getToolByName(self, 'portal_groups')
        group = grouptool.addGroup(id=group_id, title=name, description=description)
        #print "\n\n",dir(group),"\n\n"
    

    security.declarePublic('getGroups')
    def getGroups(self, parent='', prefix=''):
        """
        return a list of groups created by training centers
        """
        group_id = parent + '_' + prefix
        #print group_id
        acl_users = getToolByName(self, 'acl_users')
        groups = acl_users.searchGroups(id=group_id,sort_by='id')
        #print "getGroups: ",groups
        return groups
        
        
    security.declarePublic('removeUserGroup')        
    def removeUserGroup(self, users=[], group=''):
        """
        """
        tmp_group = group
        membership = getToolByName(self, 'portal_membership')
        grouptool = getToolByName(self, 'portal_groups')
        group = grouptool.getGroupById(group)
        for user in users:
            group.removeMember(user)
            user = membership.getMemberById(user)
            
            grps = list(user.getGroups())
            if tmp_group in grps:
                grps.remove(tmp_group)
            user.setGroups(grps)
            user.reindexObject()
        
    
    security.declarePublic('addUserGroup')
    def addUserGroup(self, users=[], group=''):
        """
        """
        tmp_group = group
        membership = getToolByName(self, 'portal_membership')
        grouptool = getToolByName(self, 'portal_groups')
        group = grouptool.getGroupById(group)
        for user in users:
            group.addMember(user)
            user = membership.getMemberById(user)
            grps = list(user.getGroups())
            if not tmp_group in grps:
                grps.append(tmp_group)
                user.setGroups(grps)
                user.reindexObject()
            

    security.declarePublic('addGroupUser')
    def addGroupUser(self, groups=[], user=''):
        """
        Obtain a list of groups and add for a user
        """
        membership = getToolByName(self, 'portal_membership')
        grouptool = getToolByName(self, 'portal_groups')
        for group in groups:
            group = grouptool.getGroupById(group)
            group.addMember(user)
        user = membership.getMemberById(user)
        user.setGroups(groups)
        user.reindexObject()
            
    security.declarePublic('removeGroupUser')
    def removeGroupUser(self, user='', groups=[]):
        """
        """
        membership = getToolByName(self, 'portal_membership')
        grouptool = getToolByName(self, 'portal_groups')
        user = membership.getMemberById(user)
        grps = list(user.getGroups())
        for group in groups:
            if group in grps:
                grps.remove(group)
            group = grouptool.getGroupById(group)
            group.removeMember(user)
        user.setGroups(grps)
        user.reindexObject()

    def importCsvUser(self, context,filename=''):
        """Así se usa tctool"""
        context = aq_inner(context)
        rows = csv.DictReader(open(os.path.join(PATH_IMPORT,filename),'r'),delimiter=';', quotechar='"')
        for count, user in enumerate(list(rows)):
            id = user['id']
            #user['mail'] = 'usuario@cecadelatam.com'
            #user['password'] = '12345678'
            user['confirm_password'] = user['password']
            #user['product'] = user['product'].split('/')
            user['company_division'] = user['company_division'].split(',')
            
            context.invokeFactory('eduMember', **user)
            obj = context._getOb(id)
            notify(ObjectInitializedEvent(obj))
            obj.reindexObject()
            
            logger.info("usuario "+str(count))
            
            if count and not count % 200:
                transaction.savepoint(optimistic=True)
                logger.info("Se envio un commit")
        transaction.savepoint(optimistic=True)
        

    def exportCsvUser(self, fields=None, delimiter='tabulator',
                      quote_char='double_quote', coding='utf-8',
                      export_type='eduMember', url=None):
        
        #portal_url = getToolByName(self, "portal_url")
        #portal = portal_url.getPortalObject()
        #container = getattr(portal, region) # note that we need use getattr because dash is invalid in syntax
        fields = ['FirstName', 'LastName','email',
                  'id',
                  #Schemata: Company
                  'company_employee_number',
                  'company_work_area','company_position',
                  'company_division','company_employee_startdate',
                  'company_employee_seniority',
                  ##Schemata: Location
                  'state','location_plaza','location_region',
                  #Schemata: Personal
                  'personal_birthdate','personal_age',
                  'personal_schooling','personal_residence',
                  'personal_phone','personal_gender',
                  'personal_last_school',
                  ]
        
        container = self.unrestrictedTraverse(url)
        contacts = container.listFolderContents(
                                                contentFilter={'portal_type':export_type}
                                                )

        # generate result
        #Header
        rows = [fields] 
        #Content
        for contact in contacts:
            row = []
            for fieldname in fields:
                field = contact.schema[fieldname]
                value = getattr(contact, field.accessor)()
                row.append(value)
            rows.append(row)
        
        # convert lists to csv string
        
        delim_map = {
         'tabulator':'\t',
         'semicolon':';',
         'colon':':',
         'comma':',',
         'space':' ',
        }

        delimiter = delim_map[delimiter]
        quote_map = {'double_quote':'"', 'single_quote':"'", }
        quote_char = quote_map[quote_char]

        
        ramdisk = StringIO()
        writer = csv.writer(ramdisk, delimiter=delimiter)
        writer.writerows(rows)
        result = ramdisk.getvalue()
        ramdisk.close()

        # encode the result
        charset = 'utf-8'
        if coding:
            result = result.decode(charset).encode(coding)
        else:
            coding = charset

        # set headers and return
        setheader = self.REQUEST.RESPONSE.setHeader
        setheader('Content-Length', len(result))
        setheader('Content-Type', 'application/vnd.ms-excel; charset=%s' % coding)
        setheader('Content-Disposition', 'filename=users_%s.dat' %(url))
        return result
        #return result.decode('utf-8').encode('latin-1')


    def exportCsvUserByGroup(self, group, fields=None, delimiter='tabulator',
                      quote_char='double_quote', coding='utf-8',
                      export_type='eduMember', url=None):

        grouptool = getToolByName(self, 'portal_groups')
        groupobj = grouptool.getGroupById(group)
        contacts = groupobj.getAllGroupMembers ()

        fields = ['FirstName', 'LastName','email',
                  'id',
                  #Schemata: Company
                  'company_employee_number',
                  'company_work_area','company_position',
                  'company_division','company_employee_startdate',
                  'company_employee_seniority',
                  ##Schemata: Location
                  'state','location_plaza','location_region',
                  #Schemata: Personal
                  'personal_birthdate','personal_age',
                  'personal_schooling','personal_residence',
                  'personal_phone','personal_gender',
                  'personal_last_school',
                  ]
        
        #~ container = self.unrestrictedTraverse(url)
        #~ contacts = container.listFolderContents(
                                                #~ contentFilter={'portal_type':export_type}
                                                #~ )
        # generate result
        #Header
        rows = [fields ] 
        #Content
        for contact in contacts:
            row = []
            for fieldname in fields:
                field = contact.schema[fieldname]
                value = getattr(contact, field.accessor)()
                row.append(value)
            rows.append(row)
            
        #Prepare call to csv writer
        delim_map = {
         'tabulator':'\t',
         'semicolon':';',
         'colon':':',
         'comma':',',
         'space':' ',
        }

        delimiter = delim_map[delimiter]
        quote_map = {'double_quote':'"', 'single_quote':"'", }
        quote_char = quote_map[quote_char]

        
        # convert lists to csv string
        ramdisk = StringIO()
        writer = csv.writer(ramdisk, delimiter=delimiter)
        writer.writerows(rows)
        result = ramdisk.getvalue()
        ramdisk.close()

        # encode the result
        charset = 'utf-8'
        if coding:
            result = result.decode(charset).encode(coding)
        else:
            coding = charset

        # set headers and return
        setheader = self.REQUEST.RESPONSE.setHeader
        setheader('Content-Length', len(result))
        setheader('Content-Type', 'application/vnd.ms-excel; charset=%s' % coding)
        setheader('Content-Disposition', 'filename=users_%s.dat' %(url))
        return result
        #return result.decode('utf-8').encode('latin-1')


registerType(TCTool, PROJECTNAME)


