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
Base classes for providing a generic SCORM-compliant API.

$Id: base.py 1952 2007-08-23 12:40:09Z helmutm $
"""

from zope import component
from zope.component import adapts
from zope import interface
from zope.interface import implements

from eduintelligent.sco.scorm.interfaces import IScormAPI
from eduintelligent.sco.scorm.interfaces import ITrackingStorage


OK = '0'

scormInteractionsPrefixes = ['cmi.interactions.']

scormChildren = {
    'cmi.comments_from_learner': ('comment', 'location', 'timestamp'),
    'cmi.comments_from_lms': ('comment', 'location', 'timestamp'),
    'cmi.interactions': ('id', 'type', 'objectives', 'timestamp',
            'correct_responses', 'weighting', 'learner_response',
            'result', 'latency', 'description'),
    'cmi.learner_preference': ('audio_level', 'language',
            'delivery_speed', 'audio_captioning'),
    'cmi.objectives': ('id', 'score', 'success_status', 'completion_status',
            'description'),
    ('cmi', 'score'): ('scaled', 'raw', 'min', 'max'),
}


################################################################
scormInteractionsPrefixes.append('yep.interactions.')

scormChildren.update({
    'yep.interactions': ('topic_id', 'question_id', 'score', 'max_duration',
            'winner_duration', 'learner_duration', 'last_question',
            'diced_number', 'next_dice_duration'),
})
################################################################


class ScormAPI(object):
    """ ScormAPI objects are temporary adapters created by
        browser or XML-RPC views.
    """

    implements(IScormAPI)
    adapts(ITrackingStorage)

    def __init__(self, context):
        self.context = context

    def init(self, taskId, runId, userId):
        self.taskId = taskId
        self.runId = runId
        self.userId = userId

    def initialize(self, parameter=''):
        # Note that the run has already been started upon SCO launch, the runId
        # usually being part of the URI or XML-RPC call arguments.
        return OK

    def terminate(self, parameter=''):
        rc = self.commit()
        if rc == OK:
            self.context.stopRun(self.taskId, self.runId)
        return rc

    def commit(self, parameter=''):
        return OK

    def setValue(self, element, value):
        tracks = self.context.getUserTracks(self.taskId, self.runId, self.userId)
        recnum = self._getRecnum(element)
        track = self._getTrack(tracks, recnum)
        data = track is not None and track.data or {}
        data[element] = value
        if track is None:
            data['recnum'] = recnum
            self.context.saveUserTrack(self.taskId, self.runId, self.userId, data)
        else:
            self.context.updateTrack(track, data)
        return OK

    def setValues(self, mapping={}, **kw):
        mapping.update(kw)
        # TODO: optimize, i.e. retrieve existing tracks only once.
        for key, value in mapping.items():
            rc = self.setValue(key, value)
            if rc != OK:
                return rc
        return OK

    def getValue(self, element):
        tracks = self.context.getUserTracks(self.taskId, self.runId, self.userId)
        if element.endswith('._count'):
            base = element[:-len('._count')]
            for prefix in scormInteractionsPrefixes:
                if element.startswith(prefix):
                    return self._countInteractionTracks(tracks), OK
            track = self._getTrack(tracks, -1)
            if track is None:
                return 0, OK
            return self._countSubelements(track.data, base), OK
        if element.endswith('_children'):
            base = element[:-len('._children')]
            return self._getChildren(base)
        recnum = self._getRecnum(element)
        track = self._getTrack(tracks, recnum)
        if track is None:
            return '', '403'
        data = track.data
        if element in data:
            return data[element], OK
        else:
            return '', '403'

    def getErrorString(self, errorCode):
        return ''

    def getDiagnostic(self, code):
        return ''

    # helper methods

    def _getRecnum(self, element):
        for prefix in scormInteractionsPrefixes:
            if element.startswith(prefix):
                # interaction record
                return int(element[len(prefix):].split('.', 1)[0])
        return -1 # base record

    def _splitKey(self, element):
        if element.startswith('cmi.interactions.'):
            parts = element.split('.')
            return '.'.join(parts[:3]), '.'.join(parts[3:])
        return '', element

    def _getTrack(self, tracks, recnum):
        for tr in tracks:
            if tr.data['recnum'] == recnum:
                return tr
        return None

    def _countSubelements(self, data, element):
        result = set()
        for key in data:
            if key.startswith(element) and key not in result:
                result.add(key)
        return len(result)

    def _countInteractionTracks(self, tracks):
        return len([tr for tr in tracks
                       if tr.data.get('recnum', -1) >= 0])

    def _getChildren(self, base):
        if base in scormChildren:
            return scormChildren[base], OK
        parts = base.split('.')
        if len(parts) >= 2:
            # this may be somewhat simplistic, but should cover the
            # most common cases
            key = (parts[0], parts[-1])
            if key in scormChildren:
                return scormChildren[key], OK
        return '', '401'

