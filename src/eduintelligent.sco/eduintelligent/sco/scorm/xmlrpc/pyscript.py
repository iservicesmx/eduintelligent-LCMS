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
XML-RPC views for calling Python scripts.

$Id: pyscript.py 2062 2007-09-21 11:23:45Z helmutm $
"""

from array import array
from zope.interface import implements
from zope.app.publisher.xmlrpc import MethodPublisher
from zope.security.proxy import removeSecurityProxy
from zope.traversing.api import getName


class PyScriptMethods(MethodPublisher):
    """ XML-RPC view class for Python script container.
    """

    def __init__(self, context, request):
        #self.context = context
        self.context = removeSecurityProxy(context) # no check atm
        self.request = request

    def getScripts(self):
        """ Return a list of dictionaries with the scripts in this
            script container.
        """
        scripts = self.context.getItems()
        return [dict(name=getName(s),
                     title=s.title or u'',
                     parameters=s.parameters or u'')
                for s in scripts]

    def call(self, name, args=[]):
        script = self.context[name]
        result = script(self.request, *args)
        return self.unwrap(result)

    def callScript(self, name, args=[]):
        return self.call(name, args)

    def unwrap(self, data):
        data = removeSecurityProxy(data)
        #print '*** data:', type(data), data
        if isinstance(data, (list, tuple, array)):
            data = [self.unwrap(element) for element in data]
        elif isinstance(data, dict):
            data = dict([(self.unwrap(k), self.unwrap(v))
                         for k, v in data.items()])
        elif data is None:
            data = 'None'
        elif isinstance(data, (int, float)):
            pass
        elif isinstance(data, basestring):
            try:
                data = float(data)
            except ValueError:
                pass
        else:
            data = [self.unwrap(element) for element in data]
        return data

