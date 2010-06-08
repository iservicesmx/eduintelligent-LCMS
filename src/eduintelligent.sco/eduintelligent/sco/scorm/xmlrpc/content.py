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

$Id: content.py 2164 2007-11-10 13:24:28Z helmutm $
"""

from zope.interface import implements
from zope.traversing.api import getName
from zope.app.publisher.xmlrpc import XMLRPCView
from zope.app.publisher.xmlrpc import MethodPublisher
from zope.security.proxy import removeSecurityProxy

identPattern = u'##ident##'


class ContentPoolMethods(MethodPublisher):
    """ XML-RPC view class for ContentPoolMethods objects.
    """

    def __init__(self, context, request):
        self.context = removeSecurityProxy(context)
        self.request = request

    def addTopic(self, text):
        """ """
        return self.context.addTopic(text)

    def setTopic(self, id, text):
        """ """
        self.context.setTopic(id, text)
        return 'OK'

    def removeTopic(self, id):
        """ """
        self.context.removeTopic(id)
        return 'OK'

    def getTopics(self):
        """ """
        for c in self.context.values():
            if c.__parent__ != self.context:
                c.__parent__ = self.context
                print '*** __parent__ changed ***', c, c.__parent__
        return dict(self.context.getTopics())

    def createItem(self, title=u'', body=u'', topics=[], format=u'text/xml'):
        """ """
        name = self.context.generateName()
        obj = self.context.createNode(name, title=title, body=body,
                                            format=format, topics=topics)
        if identPattern in body:
            obj.body = body.replace(identPattern, name)
        return name

    def createReference(self, title=u'', body=u'', pages=u'', url=u'', topics=[]):
        """ """
        name = self.context.generateName('r')
        obj = self.context.createNode(name, typeName='reference',
                                      title=title, body=body,
                                      pages=pages, url=url,
                                      format='text/plain', topics=topics)
        return name

    def removeItems(self, itemNames):
        """ """
        for name in itemNames:
            del self.context[name]
        return 'OK'

    def getItems(self, topic=None, typeName='content'):
        """ Return a sequence of dictonaries for all selected items.
        """
        topics = topic and [topic] or None
        result = []
        for node in self.context.getNodes(topics, typeName):
            entry = dict(ident=getName(node),
                         title=node.title,
                         body=node.body,
                         topics=sorted(node.topics),
                         references=sorted(node.references))
            if typeName == 'reference':
                entry['pages'] = node.pages
                entry['url'] = node.url
            result.append(entry)
        return sorted(result,  lambda a, b: cmp(a['title'], b['title']))

    def getReferences(self, topic=None):
        """ Return a sequence of Reference objects.
        """
        return self.getItems(topic, 'reference')


class ContentMethods(MethodPublisher):
    """ XML-RPC view class for Content objects.
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
        return self.context.title

    def setExplanation(self, explanation):
        """ """
        self.context.explanation = explanation
        return 'OK'

    def getExplanation(self):
        """ """
        return self.context.explanation or ''

    def setBody(self, body):
        """ """
        name = getName(self.context)
        if name and identPattern in body:
            body = body.replace(identPattern, name)
        self.context.body = body
        return 'OK'

    def getBody(self):
        """ """
        return self.context.body

    def setReferences(self, value):
        """ """
        self.context.references = value
        return 'OK'

    def getReferences(self):
        """ """
        return self.context.references

    def setTopics(self, topics):
        """ """
        self.context.topics = topics
        return 'OK'

    def getTopics(self):
        """ """
        return sorted(t for t in self.context.topics)

    def edit(self, title=u'', body=u'', topics=[], format=None):
        """ """
        self.setTitle(title)
        self.setBody(body)
        self.setTopics(topics)
        if format:
            self.setFormat(format)
        return 'OK'


class ReferenceMethods(ContentMethods):
    """ XML-RPC view class for Reference objects.
    """

    def setPages(self, value):
        """ """
        self.context.pages = value
        return 'OK'

    def getPages(self):
        """ """
        return self.context.pages or ''

    def setUrl(self, value):
        """ """
        self.context.url = value
        return 'OK'

    def getUrl(self):
        """ """
        return self.context.url or ''

    def edit(self, title=u'', body=u'', pages=u'', url=u'',
             topics=[], format=None):
        """ """
        self.setTitle(title)
        self.setBody(body)
        self.setPages(pages)
        self.setUrl(url)
        self.setTopics(topics)
        if format:
            self.setFormat(format)
        return 'OK'
