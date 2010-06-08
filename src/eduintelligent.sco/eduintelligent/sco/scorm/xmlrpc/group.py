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
XML-RPC views for group management.

$Id: group.py 1824 2007-07-13 13:32:22Z helmutm $
"""

from zope.interface import implements
from zope.app.publisher.xmlrpc import MethodPublisher
from zope.security.proxy import removeSecurityProxy
from zope.traversing.api import getName

from yeepa.xmlrpc.user import userAsDict
from yeepa.standard.group import Group


class GroupSourceMethods(MethodPublisher):
    """ XML-RPC view class for GroupSource objects.
    """

    def __init__(self, context, request):
        #self.context = context
        self.context = removeSecurityProxy(context) # no check atm
        self.request = request

    def createGroup(self, title):
        """ """
        obj = self.context.createGroup()
        obj.title = title
        return getName(obj)

    def removeGroup(self, name):
        """ """
        del self.context[name]
        return 'OK'

    def getGroup(self, name):
        """ """
        group = self.context.getGroup(name)
        return dict(ident=name, title=group.title)

    def getGroups(self):
        """ """
        return sorted(dict(ident=getName(group), title=group.title)
                      for group in self.context.getGroups())


class GroupMethods(MethodPublisher):
    """ XML-RPC view class for Group objects.
    """

    def __init__(self, context, request):
        #self.context = context
        self.context = removeSecurityProxy(context) # no check atm
        self.request = request

    def setTitle(self, title):
        """ """
        self.context.title = title
        return 'OK'

    def getTitle(self):
        """ """
        return self.context.title

    def getMembers(self):
        """ """
        userSource = self.context.getYeepa().getUserSource()
        name = getName(self.context)
        users = [u for u in userSource.getUsers(name)]
        return sorted((userAsDict(user) for user in users),
                      key=lambda x: x['nickName'])

    def addMember(self, userName):
        """ """
        self.context.addMember(userName)
        return 'OK'

    def removeMember(self, userName):
        """ """
        self.context.removeMember(userName)
        return 'OK'

