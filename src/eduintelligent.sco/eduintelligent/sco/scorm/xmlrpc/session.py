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

$Id: session.py 2156 2007-11-06 16:49:31Z helmutm $
"""

import time
from zope.interface import implements
from persistent.list import PersistentList
from zope.app.publisher.xmlrpc import MethodPublisher
from zope.security.proxy import removeSecurityProxy
from zope.traversing.api import getName

from yeepa.standard.session import Assessment, Participation


class SessionStorageMethods(MethodPublisher):
    """ XML-RPC view class for SessionStorage objects.
    """

    def __init__(self, context, request):
        self.context = removeSecurityProxy(context)
        self.request = request

    def createAssessment(self, title=u'', topics=[]):
        """ """
        obj = self.context.createItem(title=title, topics=topics)
        return getName(obj)

    def removeItems(self, itemNames):
        """ """
        for name in itemNames:
            del self.context[name]
        return 'OK'

    def getItems(self, states=None):
        """ Return a sequence of dictionaries for all items in the
            session storage. Optionally filter for the states given.
        """
        return [asDictionary(s) for s in self._getSessions(states)]

    def getAvailableAssessments(self, states=('open',)):
        """ """
        return [asDictionary(s) for s in self._getSessions()
                    if s.available(states)]

    def _getSessions(self, states=None):
        result = sorted(self.context.values(), key=lambda x: x.title)
        if states:
            if isinstance(states, basestring):
                states = [states]
            result = [s for s in result if s.state in states]
        return result


class AssessmentMethods(MethodPublisher):
    """ XML-RPC view class for Assessment objects.
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

    def getState(self):
        """ """
        return self.context.state

    def setState(self, state):
        """ """
        self.context.state = state
        return 'OK'

    def setTopics(self, topics):
        """ """
        self.context.topics = topics
        return 'OK'

    def getTopics(self):
        """ """
        return self.context.topics

    def getTopicsWithText(self):
        """ """
        cp = self.context.getYeepa().getContentPool()
        return [{'id': t,
                 'text': cp.getTopicText(t)} for t in self.context.topics]

    def getStartTime(self):
        """ """
        t = self.context.startTime
        return t and time.strftime('%Y-%m-%d %H:%M', time.localtime(t)) or ''

    def setStartTime(self, value):
        """ """
        self.context.startTime = value and int(time.mktime(
                time.strptime(value, '%Y-%m-%d %H:%M'))) or None
        return 'OK'

    def setDuration(self, duration, unit):
        """ """
        self.context.duration = duration
        self.context.durationUnit = unit
        return 'OK'

    def getDuration(self):
        """ """
        return [self.context.duration, self.context.durationUnit]

    def getSessionFormat(self):
        """ """
        return self.context.sessionFormat

    def setSessionFormat(self, format):
        """ """
        self.context.sessionFormat = format
        return 'OK'

    def getComment(self):
        """ """
        return self.context.comment

    def setComment(self, comment):
        """ """
        self.context.comment = comment
        return 'OK'

    def getInvitationMessage(self):
        """ """
        return self.context.invitationMessage

    def setInvitationMessage(self, message):
        """ """
        self.context.invitationMessage = message
        return 'OK'

    # TODO: move more of the basic participations logic to the Assessment class!

    def addParticipation(self, userId, nickName, email, topic):
        """ """
        self.context.participations.append(Participation(
                                userId, nickName, email, str(topic)))
        return len(self.context.participations) - 1

    def setParticipation(self, idx, userId, nickName, email, topic):
        """ """
        length = len(self.context.participations)
        idx = int(idx)
        if length == 0: # make sure we don't get the class's list
            self.context.participations = PersistentList()
        for i in range(length, idx+1):
            self.context.participations.append(None)
        userId = userId or 'user' + str(idx+1)
        topic = topic or (len(self.content.topics) > idx
                          and self.content.topics[idx]) or ''
        self.context.participations[idx] = Participation(
                                userId, nickName, email, str(topic))
        return 'OK'

    def getParticipation(self, idx):
        """ """
        idx = int(idx)
        if len(self.context.participations) <= idx:
            return {}
        p = self.context.participations[idx]
        if p is None:
            return {}
        return {'userId': p.userId, 'nickName': p.nickName, 'email': p.email,
                'topic': p.topic}

    def getParticipations(self):
        """ """
        length = (self.context.sessionFormat == 'multi4' and 4
                    or len(self.context.participations))
        return [self.getParticipation(idx) for idx in range(length)]

    def clear(self):
        """ """
        self.context.clear()
        return 'OK'

    def cloneAssessment(self):
        """ Returns a dictionary:
            {'id': assessmentId, 'error': message, 'errorCode': number}
        """
        return self.context.cloneAssessment()

    def inviteParticipants(self, senderEmail, senderName=None, skipSender=False):
        """ Returns a dictionary: {'error': message, 'errorCode': number}
        """
        return self.context.inviteParticipants(senderEmail, senderName,
                                request=self.request, skipSender=skipSender)


def asDictionary(session):
    return {'ident': str(getName(session)),
            'title': session.title,
            'type': 'assessment',
            'sessionFormat': session.sessionFormat,
            'state': session.state,
            'duration': [session.duration, session.durationUnit]}
