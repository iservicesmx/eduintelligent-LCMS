#
#  Copyright (c) 2005 Helmut Merz helmutm@cy55.de
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
Tournament and Assessment views.

$Id: media.py 2135 2007-10-30 14:37:23Z helmutm $
"""

from zope.interface import implements
from zope.app.publisher.xmlrpc import XMLRPCView
from zope.app.publisher.xmlrpc import MethodPublisher
from zope.dublincore.interfaces import IZopeDublinCore
from zope.security.proxy import removeSecurityProxy
from zope.traversing.api import getName

class AssetManagerMethods(MethodPublisher):
    """ XML-RPC view class for AssetManager objects.
    """

    def __init__(self, context, request):
        self.context = removeSecurityProxy(context)
        self.request = request

    def createItem(self, title=u'', format=''):
        """ """
        obj = self.context.createItem()
        obj.contentType = format
        obj.title = title
        return getName(obj)

    def removeItems(self, itemNames):
        """ """
        for name in itemNames:
            del self.context[name]
        return 'OK'

    def getItems(self, topic=None):
        """ Return a sequence of dictionaries for all items.
        """
        return sorted([{'ident': getName(item),
                        'title': self.getItemTitle(item),
                        'dimensions': item.getImageSize(),
                        'size': item.getSize()}
                            for item in self.context.values()],
                      lambda a, b: cmp(a['title'], b['title']))

    def getItemTitle(self, item):
        """ """
        title = getattr(item, 'title', None)
        if title is None:
            dc = IZopeDublinCore(item)
            title = dc.title or u''
        return title


class AssetMethods(MethodPublisher):
    """ XML-RPC view class for media assets.
    """

    def __init__(self, context, request):
        self.context = removeSecurityProxy(context)
        self.request = request

    def setTitle(self, title):
        """ """
        self.context.title = title
        return 'OK'

    def getTitle(self):
        """ """
        title = getattr(self.context, 'title', None)
        if title is None:
            dc = IZopeDublinCore(self.context)
            title = dc.title or u''
        return title

    def getSize(self):
        """ """
        return self.context.getSize()

    def getDimensions(self):
        """ """
        return self.context.getImageSize()
