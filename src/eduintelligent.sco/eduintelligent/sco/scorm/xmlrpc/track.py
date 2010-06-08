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
Tracking storage and track views.

$Id: track.py 2229 2007-12-10 11:30:12Z helmutm $
"""

from zope.interface import implements
from zope.app.publisher.xmlrpc import XMLRPCView
from zope.app.publisher.xmlrpc import MethodPublisher
from zope.security.proxy import removeSecurityProxy

from cybertools.scorm.interfaces import IScormAPI
from cybertools.tracking.btree import timeStamp2ISO


class TrackingStorageMethods(MethodPublisher):
    """ XML-RPC view class for TrackingStorage objects.
    """

    def __init__(self, context, request):
        self.context = removeSecurityProxy(context)
        self.request = request
        self.scormAPI = IScormAPI(self.context)

    def startRun(self, assessmentId):
        """ """
        return self.context.startRun(assessmentId)

    def stopRun(self, assessmentId):
        """ """
        return self.context.stopRun(assessmentId)

    # the"classical" way of storing a track

    def recordTrack(self, assessmentId, runId, userName, data):
        """ """
        self.context.saveUserTrack(assessmentId, int(runId), userName, data)
        return runId or self.context.currentRuns[assessmentId]

    # SCORM-conformant access. Note that the data given (element names
    # and values) must conform to the SCORM data model.

    def scormSetValue(self, assessmentId, runId, userName, element, value):
        """ """
        self.scormAPI.init(assessmentId, int(runId), userName)
        return self.scormAPI.setValue(element, value)

    def scormSetValues(self, assessmentId, runId, userName, mapping):
        """ """
        self.scormAPI.init(assessmentId, int(runId), userName)
        return self.scormAPI.setValues(mapping)

    def scormGetValue(self, assessmentId, runId, userName, element):
        """ """
        self.scormAPI.init(assessmentId, int(runId), userName)
        return self.scormAPI.getValue(element)

    # query methods

    def getTaskIds(self):
        """ """
        return list(self.context.getTaskIds())

    def getUserNames(self, taskId):
        """ """
        return self.context.getUserNames(taskId)

    def listTracks(self, assessmentId, userName):
        """ """
        criteria = {}
        if assessmentId:
            criteria['taskId'] = assessmentId
        if userName:
            criteria['userName'] = userName
        tracks = self.context.query(**criteria)
        return [self.trackToDict(t) for t in tracks]

    def getLastUserTrack(self, assessmentIdId, runId, userName):
        """ """
        track = self.context.getLastUserTrack(assessmentIdId, int(runId), userName)
        return self.trackToDict(track)

    def query(self, criteria):
        """ """
        if 'assessmentId' in criteria:
            criteria['taskId'] = criteria['assessmentId']
            del criteria['assessmentId']
        tracks = self.context.query(**criteria)
        return [self.trackToDict(t) for t in tracks]

    def trackToDict(self, track):
        result = track.metadata
        result['timeStamp'] = timeStamp2ISO(result['timeStamp'])
        result['assessmentId'] = result['taskId']
        result['data'] = track.data and dict(track.data) or {}
        return result

    # statistics

    def getRanking(self, assessmentId, runId=-1, maxCount=-1):
        """ """
        result = self.context.scormStats.getRanking(assessmentId, int(runId))
        maxCount = int(maxCount)
        if maxCount > 0:
            result = result[:maxCount]
        return result

    def getTotals(self):
        """ """
        return self.context.scormStats.getTotals()

    def getUserTotal(self, userName):
        """ """
        return self.context.scormStats.getUserTotal(userName)

    def getQuestionTotals(self):
        """ """
        return self.context.scormStats.getQuestionTotals()

    def getTopicTotals(self):
        """ """
        return self.context.scormStats.getTopicTotals()

    # deprecated statistics methods

    def getXRanking(self, assessmentId, runId=-1, maxCount=-1):
        """ Deprecated ranking method """
        result = self.context.statistics.getRanking(assessmentId, int(runId))
        if maxCount > 0:
            result = result[:maxCount]
        return [self.trackToDict(track) for track in result]

    def getXTotals(self):
        """ """
        return self.context.statistics.getTotals()

    def getXUserTotal(self, userName):
        """ """
        return self.context.statistics.getUserTotal(userName)

    def getXQuestionTotals(self):
        """ """
        return self.context.statistics.getQuestionTotals()

    def getXTopicTotals(self):
        """ """
        return self.context.statistics.getTopicTotals()

