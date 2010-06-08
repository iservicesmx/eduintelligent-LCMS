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
Standard implementation of the classes associated with user tracking.

$Id: track.py 2212 2007-12-04 10:00:07Z helmutm $
"""

from zope.interface import implements

from eduintelligent.sco.scorm.interfaces import ITrackingStorage, ITrack
from eduintelligent.sco.scorm.reporting import Statistics
from eduintelligent.sco.scorm import tracking
from plone.app.content import item
from plone.locking.interfaces import ITTWLockable
from plone.app.content.interfaces import INameFromTitle

class Track(tracking.Track):

    __allow_access_to_unprotected_subobjects__ = 1

    implements(ITrack)

    index_attributes = tracking.Track.index_attributes + ('contentId',)

    trackDataKeys = dict(
            contentId='cmi.interactions.%i.id',
            result='cmi.interactions.%i.result',
            score='yep.interactions.%i.score',
    )
    
    @property
    def indexdata(self):
        result = self.metadata
        data = self.data
        recnum = data.get('recnum', -1)
        result['recnum'] = recnum
        for attr, k in self.trackDataKeys.items():
            if '.%i.' in k:
                key = recnum >= 0 and k % recnum or None
            else:
                key = recnum == -1 and k
            result[attr] = key and data.get(key, None) or None
        return result


class TrackingStorage(tracking.TrackingStorage):
    """ See ITrackingStorage.
    """

    implements(ITrackingStorage)

    trackFactory = Track
    indexAttributes = Track.index_attributes
    
        
    @property
    def scormStats(self):
        return Statistics(self)


