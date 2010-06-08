#
#  Copyright (c) 2007 Helmut Merz helmutm@cy55.de
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

"""
XML-RPC views for user management.

$Id: user.py 1824 2007-07-13 13:32:22Z helmutm $
"""

from zope.interface import implements
from zope.app.publisher.xmlrpc import MethodPublisher
from zope.security.proxy import removeSecurityProxy
from zope.traversing.api import getName

from yeepa.standard.user import User


class UserSourceMethods(MethodPublisher):
    """ XML-RPC view class for UserSource objects.
    """

    def __init__(self, context, request):
        #self.context = context
        self.context = removeSecurityProxy(context) # no check atm
        self.request = request

    def authenticate(self, nickName, password):
        """ Return True if the user can be authenticated. """
        user = self.context.getUserByNickName(nickName)
        return user is not None and user.password == password

    def isNickNameAvailable(self, nickName):
        """ Return True if the nickName given is not yet taken. """
        return nickName not in self.context.nickNames

    def createUser(self, nickName, email=None, userId=None, password=None,
                   lastName=None, firstName=None, groups=[]):
        """ """
        obj = self.context.createUser(nickName)
        obj.email = email or u''
        obj.userId = userId or u''
        obj.password = password or u''
        obj.firstName = firstName or u''
        obj.lastName = lastName or u''
        name = getName(obj)
        if groups:
            gs = self.context.getYeepa().getGroupSource()
            for g in groups:
                group = gs.getGroup(g)
                if group is not None:
                    group.addMember(name)
        return name

    def removeUser(self, name):
        """ """
        self.context.removeUser(name)
        return 'OK'

    def getUser(self, userName):
        """ """
        user = self.context.getUser(userName)
        if user is None:
            return {}
        return userAsDict(user)

    def getUserByNickName(self, nickName):
        """ """
        user = self.context.getUserByNickName(nickName)
        if user is None:
            return {}
        return userAsDict(user)

    def getUsers(self, groupName=None):
        """ Return a sequence of dictonaries for all selected items.
        """
        return sorted([userAsDict(user) for user in self.context.getUsers(groupName)],
                      key=lambda x: x['nickName'])


class UserMethods(MethodPublisher):
    """ XML-RPC view class for User objects.
    """

    def __init__(self, context, request):
        #self.context = context
        self.context = removeSecurityProxy(context) # no check atm
        self.request = request

    def getData(self):
        """ """
        return userAsDict(self.context)

    def edit(self, email=None, lastName=None, firstName=None,
             userId=None, password=None, groups=[]):
        """ """
        obj = self.context
        if email: obj.email = email
        if firstName: obj.firstName = firstName
        if lastName: obj.lastName = lastName
        if userId: obj.userId = userId
        if password: obj.password = password
        if groups is not None:
            name = getName(obj)
            gs = self.context.getYeepa().getGroupSource()
            oldGroups = self.context.getGroupNames()
            for g in oldGroups:
                if g not in groups:
                    gs.getGroup(g).removeMember(name)
            for g in groups:
                if g not in oldGroups:
                    gs.getGroup(g).addMember(name)
        return 'OK'

    def getGroups(self):
        """ """
        result = []
        groupSource = self.context.getYeepa().getGroupSource()
        for g in self.context.getGroupNames():
            group = groupSource.getGroup(g)
            result.append(dict(ident=g, title=group.title))
        return sorted(result, key=lambda x: x['title'])


def userAsDict(user):
    #return dict(ident=getName(user), nickName=user.nickName,
    return dict(ident=getName(user), nickName=user.nickName,
                title=user.title, email=user.email,
                userId=user.userId,
                firstName=user.firstName, lastName=user.lastName,
                groups=sorted(user.getGroupNames()),
               )

