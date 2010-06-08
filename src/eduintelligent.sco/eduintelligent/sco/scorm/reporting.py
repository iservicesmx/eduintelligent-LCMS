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
Tracking statistics based on the SCORM data model.

$Id: track.py 2229 2007-12-10 11:30:12Z helmutm $
"""

import time
from itertools import groupby
from zope.interface import implements


class Statistics(object):

    def __init__(self, context):
        self.context = context

    def getRanking(self, taskId, runId=-1):
        ts = self.context
        if runId == 0:
            runId = ts.currentRuns.get(taskId, 0)
        criteria = dict(taskId=taskId)
        if runId > -1:
            criteria['runId'] = runId
        result = []
        tracks = sorted(ts.query(**criteria),
                        key=lambda x:(x.taskId, x.runId, x.userName))
        data = (t.indexdata for t in tracks)
        for k, g in groupby(data,
                    key=lambda x: (x['taskId'], x['runId'], x['userName'])):
            row = g.next()
            entry = dict(userName=row['userName'], runId=row['runId'],
                         scoreSum=int(row.get('score') or 0))
            for rec in g:
                entry['scoreSum'] += int(rec.get('score') or 0)
            result.append(entry)
        result.sort(key=lambda x: -x['scoreSum'])
        return result

    def getTotals(self):
        entries = {}
        tracks = self.context.values()
        data = (t.indexdata for t in tracks)
        for row in data:
            if row['recnum'] == -1:
                continue
            entry = entries.setdefault(row['userName'], UserTotal())
            entry.edit(1,
                       row.get('result') in ('correct', 'richtig') and 1 or 0,
                       int(row.get('score') or 0))
        return dict((k, entry.asDict()) for k, entry in entries.items())

    def getUserTotal(self, userName):
        entry = UserTotal()
        tracks = self.context.query(userName=userName)
        data = (t.indexdata for t in tracks)
        for row in data:
            if row['recnum'] == -1:
                continue
            entry.edit(1,
                       row.get('result') in ('correct', 'richtig') and 1 or 0,
                       int(row.get('score') or 0))
        return entry.asDict()

    def getQuestionTotals(self):
        entries = {}
        content = self.content
        data = (t.indexdata for t in self.context.values())
        for row in data:
            quId = row.get('contentId')
            if quId is not None:
                question = content.get(quId)
                entry = entries.setdefault(quId, QuestionTotal(question))
                entry.count += 1
                if row.get('result') in ('correct', 'richtig'):
                    entry.corrCount += 1
        return dict((k, entry.asDict()) for k, entry in entries.items())

    def getTopicTotals(self):
        content = self.content
        quTotals = self.getQuestionTotals()
        entries = {}
        for quData in quTotals.values():
            for topicId in quData['topics']:
                entry = entries.setdefault(topicId, Total())
                entry = entries.setdefault(topicId, {})
                entry['count'] += quData['count']
                entry['countCorrect'] += quData['countCorrect']
        for t, e in entries.items():
            e.calc()
            e['title'] = content.getTopicText(t)
        return dict((k, dict(e)) for k, e in entries.items())


# helper classes

class Total(dict):

    def __init__(self):
        self['count'] = self['countCorrect'] = 0

    def calc(self):
        self['fractionCorrect'] = int(round(float(self['countCorrect'])/
                                    float(self['count'] or 1)*100))


class UserTotal(object):

    quCount = corrCount = score = 0

    def edit(self, quCount, corrCount, score):
        self.quCount += quCount
        self.corrCount += corrCount
        self.score += score

    def asDict(self):
        fractionCorrect = int(round(float(self.corrCount)/
                                    float(self.quCount or 1)*100))
        return dict(scoreSum=self.score,
                    questionCount=self.quCount,
                    questionCountCorrect=self.corrCount,
                    questionFractionCorrect=fractionCorrect)


class QuestionTotal(object):

    count = corrCount = 0

    def __init__(self, question):
        self.question = question

    def asDict(self):
        fractionCorrect = int(round(float(self.corrCount)/
                                    float(self.count or 1)*100))
        question = self.question
        title = question is not None and question.title or ''
        topics = question is not None and list(question.topics) or []
        return dict(count=self.count,
                    countCorrect=self.corrCount,
                    fractionCorrect=fractionCorrect,
                    title=title, topics=topics)
