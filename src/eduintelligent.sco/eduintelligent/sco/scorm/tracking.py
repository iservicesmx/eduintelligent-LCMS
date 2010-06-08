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
BTree-based implementation of user interaction tracking.

$Id: btree.py 2098 2007-10-08 11:21:50Z helmutm $
"""

import time

from zope.interface import implements
from zope.app.container.btree import BTreeContainer
from zope.index.field import FieldIndex

from persistent import Persistent
from BTrees import OOBTree, IOBTree
from BTrees.IFBTree import intersection, union

from interfaces import IRun, ITrackingStorage, ITrack


class Run(object):

    implements(IRun)

    id = start = end = 0
    finished = False

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return '<Run %s>' % ', '.join((str(self.id),
                                       timeStamp2ISO(self.start),
                                       timeStamp2ISO(self.end),
                                       str(self.finished)))


class Track(Persistent):

    implements(ITrack)

    metadata_attributes = ('taskId', 'runId', 'userName', 'timeStamp')
    index_attributes = metadata_attributes

    @property
    def metadata(self):
        return dict((attr, getattr(self, attr)) for attr in self.metadata_attributes)

    indexdata = metadata

    def __init__(self, taskId, runId, userName, data={}):
        self.taskId = taskId
        self.runId = runId
        self.userName = userName
        self.timeStamp = getTimeStamp()
        self.data = data

    def update(self, newData):
        self.timeStamp = getTimeStamp()
        data = self.data
        data.update(newData)
        self.data = data

    def __repr__(self):
        md = self.metadata
        md['timeStamp'] = timeStamp2ISO(md['timeStamp'])
        return '<Track %s: %s>' % (`[md[a] for a in self.metadata_attributes]`,
                                     `self.data`)

class TrackingStorage(BTreeContainer):

    implements(ITrackingStorage)

    trackFactory = Track

    trackNum = runId = 0
    runs = None

    #indexAttributes = ('taskId', 'runId', 'userName', 'timeStamp')
    indexAttributes = Track.index_attributes

    def __init__(self, *args, **kw):
        super(TrackingStorage, self).__init__(*args, **kw)
        self.indexes = OOBTree.OOBTree()
        for idx in self.indexAttributes:
            self.indexes[idx] = FieldIndex()
        self.runs = IOBTree.IOBTree()
        self.currentRuns = OOBTree.OOBTree()
        self.taskUsers = OOBTree.OOBTree()

    def setupIndexes(self):
        changed = False
        for idx in self.indexAttributes:
            if idx not in self.indexes:
                self.indexes[idx] = FieldIndex()
                changed = True
        if changed:
            self.reindexTracks()

    def idFromNum(self, num):
        return '%07i' % (num)

    def startRun(self, taskId):
        self.runId += 1
        runId = self.runId
        self.currentRuns[taskId] = runId
        run = self.runs[runId] = Run(runId)
        run.start = run.end = getTimeStamp()
        return runId

    def stopRun(self, taskId=None, runId=0, finish=True):
        if taskId is not None:
            currentRun = self.currentRuns.get(taskId)
            runId = runId or currentRun
            if runId and runId == currentRun:
                del self.currentRuns[taskId]
        run = self.getRun(runId=runId)
        if run is not None:
            run.end = getTimeStamp()
            run.finished = finish
            return runId
        return 0

    def getRun(self, taskId=None, runId=0):
        if self.runs is None:
            self.runs = IOBTree.IOBTree()
        if taskId and not runId:
            runId = self.currentRuns.get(taskId)
        if runId:
            return self.runs.get(runId)
        return None

    def saveUserTrack(self, taskId, runId, userName, data, update=False):
        if not runId:
            runId = self.currentRuns.get(taskId) or self.startRun(taskId)
        run = self.getRun(runId=runId)
        if run is None:
            raise ValueError('Invalid run: %i.' % runId)
        run.end = getTimeStamp()
        trackNum = 0
        if update:
            track = self.getLastUserTrack(taskId, runId, userName)
            if track is not None:
                return self.updateTrack(track, data)
        if not trackNum:
            self.trackNum += 1
            trackNum = self.trackNum
            trackId = self.idFromNum(trackNum)
        track = self.trackFactory(taskId, runId, userName, data)
        self[trackId] = track
        self.indexTrack(trackNum, track)
        return trackId

    def updateTrack(self, track, data):
        trackId = str(track.__name__)
        trackNum = int(trackId)
        track.update(data)
        self.indexTrack(trackNum, track)
        return trackId

    def removeTrack(self, track):
        trackId = str(track.__name__)
        trackNum = int(trackId)
        for attr in self.indexAttributes:
            self.indexes[attr].unindex_doc(trackNum)
        if trackId in self:
            del self[trackId]
                
    def indexTrack(self, trackNum, track):
        ixd = track.indexdata
        for attr in self.indexAttributes:
            value = ixd[attr]
            if value is not None:
                self.indexes[attr].index_doc(trackNum, value)
        taskId = ixd['taskId']
        userName = ixd['userName']
        if taskId not in self.taskUsers:
            self.taskUsers[taskId] = OOBTree.OOTreeSet()
        self.taskUsers[taskId].update([userName])

    def reindexTracks(self):
        for trackId in self:
            trackNum = int(trackId)
            self.indexTrack(trackNum, self[trackId])

    def getUserTracks(self, taskId, runId, userName):
        if not runId:
            runId = self.currentRuns.get(taskId)
        return self.query(taskId=taskId, runId=runId, userName=userName)

    def getLastUserTrack(self, taskId, runId, userName):
        tracks = self.getUserTracks(taskId, runId, userName)
        if tracks:
            return sorted(tracks, key=lambda x: x.timeStamp)[-1]
        else:
            return None

    def query(self, **kw):
        result = None
        for idx in kw:
            value = kw[idx]
            if idx in self.indexAttributes:
                if type(value) not in (list, tuple):
                    value = [value]
                # TODO: handle a list of values, provide union of results
                resultx = None
                for v in value:
                    resultx = self.union(resultx, self.indexes[idx].apply((v, v)))
                result = self.intersect(result, resultx)
                #result = self.intersect(result, self.indexes[idx].apply((value, value)))
            elif idx == 'timeFrom':
                result = self.intersect(result,
                                        self.indexes['timeStamp'].apply((value, None)))
            elif idx == 'timeTo':
                result = self.intersect(result,
                                        self.indexes['timeStamp'].apply((None, value)))
            elif idx == 'timeFromTo':  # expects a tuple (from, to)
                start, end = value
                result = self.intersect(result,
                                        self.indexes['timeStamp'].apply((start, end)))
        return result and [self[self.idFromNum(r)] for r in result] or set()

    def intersect(self, r1, r2):
        return r1 is None and r2 or intersection(r1, r2)

    def union(self, r1, r2):
        return r1 is None and r2 or union(r1, r2)

    def getUserNames(self, taskId):
        return sorted(self.taskUsers.get(taskId, []))

    def getTaskIds(self):
        return self.taskUsers.keys()


def timeStamp2ISO(ts):
    return time.strftime('%Y-%m-%d %H:%M', time.gmtime(ts))

def getTimeStamp():
    return int(time.time())
