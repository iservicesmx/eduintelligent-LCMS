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
SCORM interface definitions for API_1484_11.

$Id: interfaces.py 1865 2007-08-02 20:17:41Z helmutm $
"""

from zope.interface import Interface, Attribute
from zope import schema

# user interaction tracking

class IRun(Interface):
    """ A set of interactions, sort of a session.
    """

    id = Attribute('A unique integer that identifies a run within a tracking storage')
    start = Attribute('Timestamp of run creation')
    end = Attribute('Timestamp of last interaction or of stopping the run')
    finished = Attribute('Boolean that is set to True if run was finished explicitly')


class ITrack(Interface):
    """ Result data from the interactions of a user with an task.
    """

    data = Attribute('The data for this track, typically a mapping')
    metadata = Attribute('A mapping with the track\'s metadata')
    indexdata = Attribute('A mapping with the data to be used for indexing')


class ITrackingStorage(Interface):
    """ A utility for storing user tracks.
    """

    def startRun(taskId):
        """ Create a new run for the task given and return its id.
        """

    def stopRun(taskId=None, runId=0, finish=True):
        """ Stop/finish a run.
            If the runId is 0 use the task's current run.
            If the run is the task's current one remove it from the set
            of current runs.
            Set the run's ``finished`` flag to the value of the ``finish``
            argument.
            Return the real runId; return 0 if there is no run for the
            parameters given.
        """

    def getRun(taskId=None, runId=0):
        """ Return the run object identified by ``runId``. Return None
            if there is no corresponding run.
            If ``runId`` is 0 and a ``taskId`` is given return the
            current run of the task.
        """

    def saveUserTrack(taskId, runId, userName, data, update=False):
        """ Save the data given (typically a mapping object) to the user track
            corresponding to the user name, task id, and run id given.
            If the runId is 0 use the task's current run.
            If the ``update`` flag is set, the new track updates the last
            one for the given set of keys.
            Return the new track item's id.
        """

    def query(**criteria):
        """ Search for tracks. Possible criteria are: taskId, runId,
            userName, timeFrom, timeTo.
        """

    def getUserTracks(taskId, runId, userName):
        """ Return the user tracks corresponding to the user name and
            task id given. If a 0 run id is given use the current one.
        """

    def getLastUserTrack(taskId, runId, userName):
        """ Return the last user track (that with the highest timestamp value)
            corresponding to the user name and task id given.
            If a 0 run id is given use the current one.
        """

    def getUserNames(taskId):
        """ Return all user names (user ids) that have tracks for the
            task given.
        """

    def getTaskIds():
        """ Return all ids of the tasks for which there are any tracks.
        """

    def reindexTracks():
        """ Reindexes all tracks - in case of trouble...
        """



class IScormAPI(Interface):
    """ This interface represents a server-side adapter object for a
        tracking storage and a set of key/meta data that identify a
        learner session with one or more track objects. IScormAPI objects
        are stateless, so they don't remember any values between calls.

        In addition to the standard SCORM RTS methods there is a setValues()
        method that allows setting more than one value in one call,
        probably during execution of a Commit() call on the client
        side.

        There is no method corresponding to GetLastError() as the
        methods immediately return an appropriate CMIErrorCode,
        i.e. a '0' when OK.

        Note that the names of the methods have been slightly modified
        to correspond to the Python programming style guides.
    """

    taskId = Attribute('Task ID')
    runId = Attribute('Run ID (integer)')
    userId = Attribute('User ID')

    def init(taskId, runId, userId):
        """ Set the basic attributes with one call.
        """

    def initialize(parameter):
        """ Corresponds to API.Initialize('').
            Return CMIErrorCode.
        """

    def commit(parameter):
        """ Corresponds to API.Commit('').
            Return CMIErrorCode.
        """

    def terminate(parameter):
        """ Corresponds to API.Initialize('').
            Mark the run as finished.
            Return CMIErrorCode.
        """

    def setValue(element, value):
        """ Corresponds to API.SetValue(element, value).
            Return CMIErrorCode.
        """

    def setValues(mapping={}, **kw):
        """ Combine the mapping and kw arguments setting up a series of
            element-value mappings that will in turn be applied to a
            series of setValue() calls.
            Return CMIErrorCode.
        """

    def getValue(element):
        """ Corresponds to API.GetValue(element).
            Return a tuple with the current value of the element given
            (a string, '' if not present) and a CMIErrorCode.
        """

    def getErrorString(errorCode):
        """ Corresponds to API.GetErrorString(errorCode).
            Return the error text belonging to the errorCode
            (a CMIErrorCode value) given.
        """

    def getDiagnostic(code):
        """ Corresponds to API.GetDiagnostic(code).
            Return an LMS-specific information text related to the code given;
            code may but need not be a CMIErrorCode value.
        """
