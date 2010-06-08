# -*- coding: utf-8 -*-
#
# File: content.py
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

#### Standard Python modules
import os
import re
from StringIO import StringIO

#### Standard Zope modules
from zope.interface import implements
from zope.component.factory import Factory
from zope.annotation.interfaces import IAnnotations

#### Standard Products Plone
from Products.CMFCore.utils import getToolByName
from plone.locking.interfaces import ITTWLockable
from plone.app.content.interfaces import INameFromTitle
from plone.app.content.item import Item

#### 3rd Products imports

#### Local modules
from eduintelligent.sco import scoMessageFactory as _
from eduintelligent.sco.interfaces import ISCO
from eduintelligent.sco.config import PROJECTNAME, SCORM_STORE, EXTERNA_URL
from eduintelligent.sco import utilities
from eduintelligent.sco.scorm.imsmanifest import IMSManifest
from eduintelligent.sco.scorm.scormapi import ScormAPI
from eduintelligent.sco.scorm.track import TrackingStorage
from eduintelligent.sco.scorm.tracking import timeStamp2ISO


TRACK_KEY = 'eduintelligent.sco.track'


mask = re.compile(r"^([0-9]{2,4}):([0-9]{2}):([0-9]{2}).?([0-9]?[0-9]?)$")

def toInt(num):
    if num == '':
        return 0
    return int(num)

def addScormTime(time1, time2):
            
    hours1,minutes1,secondes1,primes1 = map(toInt, mask.match(time1).groups())

    hours2,minutes2,secondes2,primes2 = map(toInt, mask.match(time2).groups())
    
    # calculate the resulting added hours, secondes, ... for result

    primesReport = False;
    secondesReport = False;
    minutesReport = False;
    hoursReport = False;

    #calculate primes
    if primes1 == '':
        primes1 = 0
    if primes2 == '':
        primes2 = 0
        
    if primes1 < 10: primes1 = primes1*10
    if primes2 < 10: primes2 = primes2*10
    total_primes = primes1 + primes2;
    if total_primes >= 100:
        total_primes -= 100;
        primesReport = True;

    #calculate secondes
    total_secondes = secondes1 + secondes2
    if primesReport: total_secondes += 1
    if total_secondes >= 60:
        total_secondes -= 60;
        secondesReport = True;

    #calculate minutes
    total_minutes = minutes1 + minutes2
    if secondesReport: total_minutes += 1
    if total_minutes >= 60:
        total_minutes -= 60
        minutesReport = True
        
    #calculate hours
    total_hours = hours1 + hours2
    if minutesReport: total_hours += 1
    if total_hours >= 10000:
        total_hours -= 10000
        hoursReport = True

    #construct and return result string
    total_time = "%02d:%02d:%02d.%02d"%(total_hours, total_minutes,total_secondes,total_primes)

    return total_time



class SCO(Item):
    implements(ISCO, ITTWLockable, INameFromTitle)
    portal_type = "SCO"
    
    title = u""
    description = u""
    filename = u""
    #track = None
    
    def __init__(self, id=None):
        super(SCO, self).__init__(id)
        # annotations = IAnnotations(self)
        # try:
        #     TRACK_KEY = self.UID()
        #     print 'TRACK_KEY',TRACK_KEY
        # except:
        #     TRACK_KEY = 'eduintelligent.sco.track'
        # self.track = annotations.setdefault(TRACK_KEY, TrackingStorage())
        self.track = TrackingStorage()
    
    # @property
    # def track(self):
    #     annotations = IAnnotations(self)
    #     TRACK_KEY = self.UID()
    #     print 'TRACK_KEY',TRACK_KEY
    #     return annotations.setdefault(TRACK_KEY, TrackingStorage())

    def getUrlContents(self):
        """
        """
        scoId = "/".join(self.getPhysicalPath())
        return EXTERNA_URL + scoId

    def storePathSCO(self):
        """
        """
        scoId = "/".join(self.getPhysicalPath())
        path = os.path.join(SCORM_STORE, scoId.lstrip('/'))
        return path

    def protectDirs(self):
        """
        :> robots.txt
        User-agent: *    # aplicable a todos
        Disallow: /      # impide la indexacion de todas las paginas
        ##################################
        :> .htaccess
        chmod 644 .htaccess
        IndexIgnore *
        """
        def walker(directory):
            for name in os.listdir(directory):
                path = os.path.join(directory,name)
                if os.path.isdir(path):
                    f = open(os.path.join(path,'robots.txt'),'w')
                    f.write("""User-agent: *\nDisallow: /
                    """)
                    f.close()
                    f = open(os.path.join(path,'.htaccess'),'w')
                    f.write("""IndexIgnore *\n""")
                    f.close()
                    walker(path)
                    os.chmod(os.path.join(path,'robots.txt'), 0644)
                    os.chmod(os.path.join(path,'.htaccess'), 0644)

        scoId = "/".join(self.getPhysicalPath())
        path = os.path.join(SCORM_STORE, scoId.lstrip('/'))
        walker(path)

    def uploadContentPackage(self):
        """
        this is an event after create or edit 
        """
        specificPath = self.storePathSCO()
        print "Ruta en donde se almacena: ", specificPath
        if hasattr(self.filename,'data'):
            if os.path.exists(specificPath):
                # we want to replace an existing directory:
                utilities.removeDirectory(specificPath)
            
            utilities.createDirectory(specificPath)        

            utilities.unzip().extract(StringIO(str(self.filename.data)),specificPath)
            self.protectDirs()  ### create files to protect the public files

        self._v_manifest = None   # invalidate manifest after upload
        self._v_itemCount = None
        self.filename = None


    def getFileFromContentPackage(self, subpath, doStream=False):
        path = os.path.join(self.storePathSCO(), subpath)
        if not os.path.exists(path):
            print "cuidado, no existe el archivo!!"
            return ''
        f = open(path)
        return f.read()


    # IMS and SCORM stuff:

    _v_manifest = None
    _v_itemCount = None

    def getManifest(self):
        if self._v_manifest is None:
            xml = self.getFileFromContentPackage('imsmanifest.xml')
            if xml:
                self._v_manifest = IMSManifest(xml)
        return self._v_manifest

    def getReportData(self):
        result = []
        manifest = self.getManifest()
        # student is the student belonging to studentId or the currently loggend-in user:
        #student = wbt.getStudent(self.studentId)
        #studentName = student and student.Title() or None
        if manifest:
            for org in self.getOrganizations():
                orgTitle = self.getObjTitle(org)
                showOrgTitle = True
                for item in manifest.getSubItems(org):
                    itemId = manifest.getIdentifier(item)
                    itemIder = manifest.getItemIdentifier(itemId)
                    row = { 'orgTitle': showOrgTitle and orgTitle or '',
                            'itemId': itemId,
                            'itemTitle': manifest.getTitle(item),
                            'itemLevel': manifest.getLevel(org, item),
                            'isStartable': itemIder,
                            'startResource': manifest.getStartResource(itemIder),
                            #'student': student,
                    }
                    showOrgTitle = False  # only show on first line
                    result.append(row)
        return result

    ##############################
    #    IMS Manifest Methods
    ##############################
    def getOrganizations(self):
        """
        at same time update the variable volatile self._v_manifest
        """
        manifest = self.getManifest()
        return manifest.getOrganizations()

    def getObjTitle(self, obj):
        return self._v_manifest and self._v_manifest.getTitle(obj) or ''

    def getItemCount(self):
        return self._v_manifest and self._v_manifest.getItemCount() or 0

    def getItemTitle(self, item=0):
        return self._v_manifest and self._v_manifest.getItemTitle(item) or ''

    def getMasteryScore(self, item=0):
        return self._v_manifest and self._v_manifest.getMasteryScore(item) or ''

    def getLaunchData(self, item=0):
        return self._v_manifest and self._v_manifest.getLaunchData(item) or ''

    def getItemIndex(self, itemId):
        return self._v_manifest and self._v_manifest.getItemIndex(itemId)

    def getItems(self, documentNode):
        return self._v_manifest and self._v_manifest.getItems(documentNode)

    def getTitle(self, nodeElem):
        return self._v_manifest and self._v_manifest.getTitle(nodeElem)

    def getIdentifier(self, nodeElem):
        return self._v_manifest and self._v_manifest.getIdentifier(nodeElem)

    def getIdentifierRef(self, nodeElem):
        return self._v_manifest and self._v_manifest.getIdentifierRef(nodeElem)

    #######################
    # SCORM Stuff
    #######################
    scormElements = {
        'cmi.core._children': 'student_id,student_name,lesson_location,credit,'
                'lesson_status,entry,score,total_time,lesson_mode,exit,session_time',
        'cmi.core.score._children': 'raw,min,max',
        #replace with current data:
        'cmi.core.student_name': 'Unknown',
        'cmi.core.student_id': 'unknown',
        'cmi.core.credit': 'credit', # should depend on lesson_mode
        'cmi.core.lesson_mode': 'normal',
        #take from manifest:
        #'cmi.student_data.mastery_score': '',
        'cmi.launch_data': '',
        #replace with actuall data from lmca:
        'cmi.core.lesson_location': '',
        'cmi.core.lesson_status': 'not attempted',
        'cmi.core.entry': 'ab-initio',
        'cmi.core.score.raw':'0',
        'cmi.core.score.min': '',
        'cmi.core.score.max': '',
        'cmi.core.total_time': '0000:00:00.00',
        'cmi.core.session_time': '0000:00:00.00',
        'cmi.core.exit': '',
        'cmi.suspend_data': '',
        'cmi.comments': '',
        'cmi.comments_from_lms': '',
    }

    def getScormData(self, memberId=None, item=None):
        studentName, studentId = self.getAuthenticatedNameAndId(memberId)
        manifest = self.getManifest()
        elements = self.scormElements.copy()
        elements['cmi.core.student_id'] = studentId
        elements['cmi.core.student_name'] = studentName
        elements['cmi.launch_data'] = manifest.getLaunchData(item)
        # content must not set mastery score
        mastery = manifest.getMasteryScore(item)
        if (mastery !='not found'  and  mastery !='Item not found'):
            elements['cmi.student_data.mastery_score'] = mastery
        try:
            trackData = self.getLastUserTrack(item, 0, studentId)
            print "trackData",trackData
            elements.update(trackData['data'])
        except:
            print "\n\n\n################### el usuario", studentId, "no tiene registros"

        return elements

    def saveToUserTrack(self, data, memberId=None, item=None):
        """ Store data (a mapping) in the user's scorm track. """
        studentName, studentId = self.getAuthenticatedNameAndId(memberId)
        if studentId is None:
            return {}
        # setting lesson status
        self.setLessonStatus(data, self.getScormData(memberId, item))
        
        data['cmi.core.entry'] = 'resume'
        
        data['cmi.core.total_time'] = addScormTime(data['cmi.core.total_time'], data['cmi.core.session_time'])
        
        self.recordTrack(item, 0, studentId, data)
        
    def setLessonStatus(self, data, scormData):
        status = data.get('cmi.core.lesson_status', None)
        entry = scormData.get('cmi.core.entry', 'resume')
        if status is None \
                and scormData.get('cmi.core.lesson_mode', 'normal') == 'browse':
            status = 'browsed'
        if status is None:
            score = self._scormData.get('cmi.core.score.raw', '')
            masteryScore = scormData['cmi.student_data.mastery_score']
            if masteryScore != '' and score != '' and int(score) >= int(masteryScore):
                status = 'passed'
        if status is None:
            if scormData.get('self.cmi.core.exit', '') == 'suspend':
                status = 'incomplete'
            # not yet supported by 21LL AK:
            #elif masteryScore != '' and score != '' and int(score) < int(masteryScore):
            #    status = 'failed'
            else:
                status = 'browsed'
        data['cmi.core.lesson_status'] = status
        if status in ('complete', 'passed', 'failed'):
            entry = ''
        else:
            entry = 'resume'
        # maybe the best solution:
        #entry = ''
        #entry = 'ab-initio'
        data['cmi.core.entry'] = entry
        return data     
        
    def startRun(self, assessmentId):
        """ """
        return self.track.startRun(assessmentId)

    def stopRun(self, assessmentId):
        """ """
        return self.track.stopRun(assessmentId)

    # the"classical" way of storing a track

    def recordTrack(self, assessmentId, runId, userName, data):
        """ """
        print "recordTrack",self.track
        print "recordTrack(data)",data
        self.track.saveUserTrack(assessmentId, int(runId), userName, data)
        return runId or self.track.currentRuns[assessmentId]

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
        return list(self.track.getTaskIds())

    def getUserNames(self, taskId):
        """ """
        return self.track.getUserNames(taskId)

    def listTracks(self, assessmentId, userName):
        """ """
        criteria = {}
        if assessmentId:
            criteria['taskId'] = assessmentId
        if userName:
            criteria['userName'] = userName
        tracks = self.track.query(**criteria)
        return [self.trackToDict(t) for t in tracks]

    def getLastUserTrack(self, assessmentIdId, runId, userName):
        """ """
        track = self.track.getLastUserTrack(assessmentIdId, int(runId), userName)
        return self.trackToDict(track)

    def query(self, criteria):
        """ """
        if 'assessmentId' in criteria:
            criteria['taskId'] = criteria['assessmentId']
            del criteria['assessmentId']
        tracks = self.track.query(**criteria)
        return [self.trackToDict(t) for t in tracks]

    def trackToDict(self, track):
        result = track.metadata
        result['timeStamp'] = timeStamp2ISO(result['timeStamp'])
        result['assessmentId'] = result['taskId']
        result['data'] = track.data and dict(track.data) or {}
        return result

        ######################################
        # User Authentication
        ######################################

    def getAuthenticatedNameAndId(self, memberId=None):
        """
        """
        memberName = "??????"
        portal_membership = getToolByName(self, 'portal_membership')
        if memberId:
            member = portal_membership.getMemberById(memberId)
        else:
            member = portal_membership.getAuthenticatedMember()

        if member is not None:
            memberId = member.getId()
            memberName = member.getProperty('fullname') or memberName
            memberName = memberName.split(' ')[0]

        return memberName, memberId
    
scoFactory = Factory(SCO, title=_(u"Create a new SCO"))
