# -*- coding: utf-8 -*-
"""Definition of the Exam content type.
"""
from DateTime import DateTime
import random
import time

from zope.interface import implements
from zope.component import getUtility

from Products.ATContentTypes.content import folder
from Products.CMFCore.utils import getToolByName

from eduintelligent.evaluation.interfaces import IEvaluation, IQuestion
from eduintelligent.evaluation.config import PROJECTNAME
from eduintelligent.evaluation import evaluationMessageFactory as _

### SCORM ###
#from eduintelligent.sco.scorm.interfaces import IScormAPI
#from eduintelligent.sco.scorm.scormapi import ScormAPI
from eduintelligent.sco.scorm.track import TrackingStorage
from eduintelligent.sco.scorm.tracking import timeStamp2ISO

### Messages ###
from eduintelligent.messages.interfaces import IMessagesManager

from statistics import Statistics

TRACK_ATTRIBUTE = 'track'

# replace by: form itertools import groupby
class groupby(dict):
    def __init__(self, seq, key=lambda x:x):
        for value in seq:
            k = key(value)
            self.setdefault(k, []).append(value)
    __iter__ = dict.iteritems

class Evaluation(folder.ATFolder):
    """Contains multiple questions.
    """
    implements(IEvaluation)
    _at_rename_after_creation = True

    def __init__(self, id=None):
        super(Evaluation, self).__init__(id)
        self.track = TrackingStorage()
        #self.scormAPI = IScormAPI(self.track)

    def initTrack(self):
        if not hasattr(self, TRACK_ATTRIBUTE):
            setattr(self, TRACK_ATTRIBUTE, TrackingStorage())
        #if not hasattr(self, 'scormAPI'):    
        #    self.scormAPI = IScormAPI(self.track)

    def getNumberUserQuestion(self):
        questions = self.getNumberOfRandomQuestions()

        if questions > 0:
            return questions

        return len(self.objectIds())

    def generateQuestions(self):
        randomize = self.isRandomOrder()
        limit = self.getNumberOfRandomQuestions()

        questions = self.objectIds()
        #print "query results",results
        #questions = list(results)
        if randomize:
            #questions = list(results)
            questions.sort(lambda x,y: cmp(random.randint(0,200),100))

        if limit > 0:
            questions = questions[:limit]

        return questions


    cmi_interactions = ('id', 'type', 'time', 'weighting', 'student_response','result', 'latency', 'comments')

    def generateEvaluation(self):
        data = {}
        for i,q in enumerate(self.generateQuestions()):
            for key in self.cmi_interactions:
                keyId = "question.%s.%s"%(i,key)
                data[keyId] = ''
                if key == 'id':
                    data[keyId] = q
        data['evaluation.open'] = 0
        data['evaluation.scored'] = 0
        data['evaluation.score'] = 0
        data['evaluation.scored_extra'] = False
        data['evaluation.score_extra'] = 0.0
        data['evaluation.start'] = time.time()
        data['evaluation.end'] = 0
        print "generateEvaluation",data
        return data


    def getEvaluation(self, userId=None):
        """ 
        returns the track's runId 
        if is None the user don't have more opportunities
        """
        taskId = self.getId()
        if not userId:
            userId = self.AuthenticatedMember()

        track = self.track.getLastUserTrack(taskId,0,userId)

        if track and not track.data['evaluation.end'] and not track.data['evaluation.scored']:
            return track.data

        # revisar el numero de oportunidades
        # si el # de oportunidades es mmenor o igual no generar nada    
        data = self.generateEvaluation()
        self.track.saveUserTrack(taskId, 0, userId, data)
        return data

    def getEvaluationDetails(self, userId=None, numeval=None):

        if not userId or not numeval:
            return {},[]
        data_eval = {}
        data_interactions = []
        tracks = self.track.getUserTracks(self.getId(), 0, userId)
        if not tracks:
            return {},[]

        num = int(numeval) - 1
        evaluation = sorted(tracks, key=lambda x: x.timeStamp)[num]
        correct_responses = 0
        #print evaluation.data
        data_eval['start'] = self.utilConvertTime(evaluation.data['evaluation.start'])
        data_eval['end'] = self.utilConvertTime(evaluation.data['evaluation.end'])
        data_eval['period'] = self.utilCalculeTime(evaluation.data['evaluation.start'], evaluation.data['evaluation.end'])
        data_eval['score'] = evaluation.data['evaluation.score']
        data_eval['scored'] = evaluation.data['evaluation.scored']
        data_eval['open'] = evaluation.data['evaluation.open']
        data_eval['total_questions'] = (len(evaluation.data)-5)/8
        for e in range(data_eval['total_questions']):
            tmp = {}
            tmp['index'] = e + 1
            tmp['type'] = evaluation.data['question.%s.type'%e]
            tmp['time'] = self.utilConvertTimeHM(evaluation.data['question.%s.time'%e])
            tmp['latency'] = evaluation.data['question.%s.latency'%e]
            tmp['result'] = evaluation.data['question.%s.result'%e]
            if tmp['result']:
                correct_responses += 1
            tmp['weighting'] = evaluation.data['question.%s.weighting'%e]
            tmp['comments'] = evaluation.data['question.%s.comments'%e]

            obj = self._getOb(evaluation.data['question.%s.id'%e])
            tmp['question'] = obj.Title()

            tmp['student_response'] = evaluation.data['question.%s.student_response'%e]

            if tmp['type'] == 'choice':
                if not tmp['student_response']:
                    tmp['student_response'] = _("You did not respond within the time of question")
                    tmp['correct_response'] = ''
                else:
                    tmp['student_response'] = ', '.join(obj.getAnswerTitles(evaluation.data['question.%s.student_response'%e]))
                    tmp['correct_response'] = ', '.join(obj.getCorrectAnswerTitles())

            data_interactions.append(tmp)

        data_eval['correct_responses'] = correct_responses
        data_eval['evaluation.score_extra'] = evaluation.data['evaluation.score_extra']
        data_eval['evaluation.scored_extra'] = evaluation.data['evaluation.scored_extra']

        return data_eval,data_interactions

    def getScoreStatus(self, scored=None, score=None):
        if not scored:
            return _("Pending")

        if score < self.getMinScoreGrade():
            return _("Unapproved")

        return _("Approved")


    def getLastEvaluation(self, userId=None):
        taskId = self.getId()

        if not userId:
            userId = self.AuthenticatedMember()
        
        track = self.track.getLastUserTrack(taskId,0,userId)
        if track:
            return track.data
        return {}


    def saveUserResponse(self, data ,userId=None):
        taskId = self.getId()

        if not userId:
            userId = self.AuthenticatedMember()

        track = self.track.getLastUserTrack(taskId, 0, userId)
        if track is not None:
            return self.track.updateTrack(track, data)
        #self.track.saveUserTrack(taskId, 0, userId, data, update=True)


    def getDataUserId(self, runId, userId=None):
        if not userId:
            userId = self.AuthenticatedMember()

        track = self.track.getLastUserTrack(self.getId(), runId, userId)
        #print " getDataUserId ",track.data
        return track.data

    def getDataEvaluations(self, userId=None):
        if not userId:
            userId = self.AuthenticatedMember()
        tracks = self.track.getUserTracks(self.getId(), 0, userId)
        if tracks:
            ### Note: se tuvo que poner estas lineas para correguir el error de que un examen no tenga datos completos
            ###       esto sucede cuando un usuario inicia un examen dos veces el la mima hora y no ha terminado uno
            # for track in tracks:
            #     if len(track.data) < len(self.generateEvaluation()):
            #         return []
            return sorted(tracks, key=lambda x: x.timeStamp)
        return []

    def calculateScore(self, data):
        keys = len(data) # 
        interactions = (keys-5)/8  # 5 is evaluation data and 8 is the key of one interaction
        total_weigthing = self.getTotalWerighting(data)
        correct_answers = 0
        for e in range(interactions):
            result = data['question.%s.result'%e]
            if result:
                weighting = data['question.%s.weighting'%e]
                correct_answers += weighting        

        score_ratio = round((float(correct_answers)*100.0)/total_weigthing,2)
        return score_ratio

    def getTotalWerighting(self, data):
        return sum([self._getOb(data[i]).getWeighting() for i in data.keys() if i.endswith('.id')])            

    def formatTimeLeft(self, userId=None):
        if self.getMaxTimeResponseTest() <= 0 : return ''
        if not userId:
            userId = self.AuthenticatedMember()

        last = self.track.getLastUserTrack(self.getId(), 0, userId)
        testInfo = last.data.get('evaluation.start',time.time())

        secondsPassed = time.time() - testInfo
        secondsLeft = self.getMaxTimeResponseTest() * 60 - secondsPassed

        seconds = secondsLeft % 60
        minutes = (secondsLeft / 60) % 60
        hours   = secondsLeft / 3600

        return "%02d:%02d:%02d" % (hours, minutes, seconds)

    def getAllDataUsers(self):
        result = []
        tracks = sorted(self.track.values(),key=lambda x: x.userName)
        for track in tracks:
            tmp = {}
            tmp['userid'] = track.userName
            tmp['score'] = track.data['evaluation.score']
            tmp['start'] = self.utilConvertTime(track.data['evaluation.start'])
            tmp['end'] = self.utilConvertTime(track.data['evaluation.end'])
            tmp['time'] = self.utilCalculeTime(track.data['evaluation.start'], track.data['evaluation.end'])
            tmp['member'] = self.AuthenticatedMemberById(tmp['userid'])
            result.append(tmp)
        return result

    def getGroupDataUsers(self):

        results = []

        for k, g in groupby(self.track.values(), key=lambda r: r.userName):
            tmp = {}
            tmp['userid'] = k

            average = 0
            count = 0.0
                
            for data in g:
                #Let's fake data. This is quite, quite wrong!!!
                if not data.data.get('evaluation.scored_extra'):
                    scored_extra = False
                    score_extra = 0.0
                else:
                    scored_extra = data.data['evaluation.scored_extra']
                    score_extra = data.data['evaluation.score_extra']
                #Ends bad,dirty,evil hack

                if data.data['evaluation.scored']:
                    average += data.data['evaluation.score']
                    count += 1.0

            if not count:
                count = 1.0

            tmp['average'] = round(average/count,2)
            tmp['oportunities'] = range(1,len(g)+1)
            tmp['member'] = self.AuthenticatedMemberById(k)
            last_track = sorted(g, key=lambda x: x.timeStamp)[-1]
            tmp['score'] = last_track.data['evaluation.score']
            tmp['score_extra'] = score_extra
            tmp['scored_extra'] = score_extra
            tmp['start'] = self.utilConvertTime(last_track.data['evaluation.start'])
            tmp['end'] = self.utilConvertTime(last_track.data['evaluation.end'])
            tmp['time'] = self.utilCalculeTime(last_track.data['evaluation.start'], last_track.data['evaluation.end'])


            results.append(tmp)

        return results

    def getPendingGradeUsers(self):
        result = []
        tracks = sorted(self.track.values(),key=lambda x: x.userName)
        for track in tracks:
            if not track.data['evaluation.scored'] and track.data['evaluation.open']:            
                tmp = {}
                tmp['userid'] = track.userName
                tmp['score'] = track.data['evaluation.score']
                tmp['start'] = self.utilConvertTime(track.data['evaluation.start'])
                tmp['end'] = self.utilConvertTime(track.data['evaluation.end'])
                tmp['time'] = self.utilCalculeTime(track.data['evaluation.start'], track.data['evaluation.end'])
                tmp['member'] = self.AuthenticatedMemberById(tmp['userid'])
                result.append(tmp)
        return result

    def getOpenEvaluation(self, userId=None):
        results = []
        evaluation = self.getLastEvaluation(userId)
        total_questions = (len(evaluation)-5)/8
        for e in range(total_questions):
            if evaluation['question.%s.type'%e] == 'fill-in':
                question = {}
                question['index'] = e
                question['student_response'] = evaluation['question.%s.student_response'%e]
                question['time'] = self.utilConvertTimeHM(evaluation['question.%s.time'%e])
                question['weighting'] = evaluation['question.%s.weighting'%e]
                question['latency'] = evaluation['question.%s.latency'%e]
                qid = evaluation['question.%s.id'%e]
                question['title'] = self._getOb(qid).Title()

                result = evaluation['question.%s.result'%e]

                if result == '':
                    results.append(question)

        return results

    def setOpenEvaluation(self, data, userId=None):
        evaluation = self.getLastEvaluation(userId)
        self.saveUserResponse(data)
        pass

    def getPendingUsers(self):
        users_evaluation = [x['userid'] for x in self.getGroupDataUsers()]
        parent = self.aq_inner.aq_parent     ## verificar que es un ExamContent
        parent = parent.aq_inner.aq_parent   ## verificar que es un Course
        users_course = parent.getRegisteredStudents()
        a = frozenset(users_course)
        b = frozenset(users_evaluation)
        c = a - b
        result = []
        for user in list(c):
            member = self.AuthenticatedMemberById(user)
            result.append(member)
        return result

    def utilCalculeTime(self, time1, time2):
        if not time1 or not time2:
            return "0"

        time1 = int(time1)
        time2 = int(time2)
        totalseconds = time2 - time1
        seconds = totalseconds % 60
        minutes = (totalseconds / 60) % 60
        hours   = totalseconds / 3600
        return "%02d:%02d:%02d" % (hours, minutes, seconds)

    def utilConvertTime(self, time1):
        if not time1:
            return "0"
        time1 = time.localtime(float(time1))
        time1 = time.strftime('%d/%m/%Y - %H:%M', time1)
        return time1

    def utilConvertTimeHM(self, time1):
        if time1 == '':
            time1 = 0.0
        n = float(time1)/1000.0
        time1 = time.localtime(n)
        time1 = time.strftime('%H:%M:%S', time1)
        return time1


    def haveOpportunity(self):
        # si sus evaluacions es menor al permitido
        # si el examen no esta vencido
        if len(self.getDataEvaluations()) < self.getMaxOpportunityTest():
            return True
        return False

    def haveTime(self):
        now            = DateTime()
        startPublished = self.getInitDate()
        endPublished   = self.getFinishDate()
        if((startPublished != None) and (startPublished > now)):
            return False
        if((endPublished != None) and (now > endPublished)):
            return False
        return True

    def passEvaluation(self, userId=None):
        data = self.getLastEvaluation(userId)
        if not data:
            return False

        if data['evaluation.open'] and not data['evaluation.scored']:
            return True

        if data['evaluation.score'] < self.getMinScoreGrade():
            return False

        return True

    def AuthenticatedMember(self):
        portal_membership = getToolByName(self, 'portal_membership')
        return portal_membership.getAuthenticatedMember().getId()

    def AuthenticatedMemberById(self, userId=None):
        portal_membership = getToolByName(self, 'portal_membership')

        if not userId:
            return portal_membership.getAuthenticatedMember()

        member = portal_membership.getMemberById(userId)

        # Hack temporal que corrige error cuando un usuario es eliminado
        if not member:
            class Member:
                def getFullname(self):
                    return '--'
                def getPositionName(self):
                    return '--'
                def getPlace(self):
                    return '--'
                def getProductName(self):
                    return ['--',]
                def getDivisionName(self):
                    return ['--',]
                def getDistrict(self):
                    return '--'
                def getRegion(self):
                    return '--'
                def getEmployee(self):
                    return '--'
                def getIngress(self):
                    return '--'
                def getCountryName(self):
                    return '--'
                def getState(self):
                    return '--'
                def getCity(self):
                    return '--'
                def getPlace(self):
                    return '--'

            member = Member()

        return member

    def sendMessage(self, data=None, isOpen=False, userId=None):
        manager = getUtility(IMessagesManager)
        receiver = sender = self.AuthenticatedMember()
        if userId:
            receiver = userId
        subject = _(u"Exam name: ") + self.Title()
        normal = _(u"Your grade is: ") + str(data['evaluation.score'])
        openbody = _(u"The instructor has reviewed your exam and your grade was ")  + str(data['evaluation.score'])
        link = _(u"To see the details of this revision, please follow this link: ") + "<a href=%s target=_blank> %s </a>"%(self.absolute_url(),self.Title())
        body = normal + link
        if isOpen:
            body = openbody + link

        manager.message_new(2, sender, receiver, subject, body)

    def setScoreKardex(self, data, userId=None):
        ## validate if the user is a eduMember or has kardex attribute
        member = self.AuthenticatedMemberById(userId)
        end = self.utilConvertTime(data['evaluation.end'])
        member.setDynamicKardex(evaluation=self.getEvaluationNameAndLink(),
                                date=end,
                                course=self.getCourseName(),
                                score=str(data['evaluation.score']),
                                type='exam')

        pass

    def getCourseName(self):
        parent = self.aq_inner.aq_parent     ## verificar que es un ExamContent
        parent = parent.aq_inner.aq_parent   ## verificar que es un Course
        return parent.Title()

    def getEvaluationNameAndLink(self):
        return self.Title() + '|' + self.absolute_url()

    #############
    # Statistics
    #############
    def getExamStatistics(self, attemp=0):
        sample = []
        for userid, g in groupby(self.track.values(), key=lambda r: r.userName):
            ## !!!! check if have more than one for filter the attemp
            data = sorted(g, key=lambda x: x.timeStamp)[attemp] # filter the attemp

            if data.data['evaluation.scored']:
                sample.append(data.data['evaluation.score'])

        if not sample:
            sample = [0]
            
        return Statistics(sample)


    def getQuestionsStatistics(self, attemp=0):
        """
        obtener todas las preguntas del examen
        crear diccionario con qid, question, correct, incorrect
        agregarlo a una lista

        """
        catalog = getToolByName(self, 'portal_catalog')
        return [ dict(qid=question.getId,
                      title=question.Title,
                      counts=self.getCountUserQuestions(question.getId, attemp=attemp))
                 for question in 
                 catalog(path=dict(query='/'.join(self.getPhysicalPath()),
                                   depth=1),)
                 ]


    def getCountUserQuestions(self, qid, attemp=0):
        correct = []
        incorrect = []

        for userid, g in groupby(self.track.values(), key=lambda r: r.userName):
            ## !!!! check if have more than one for filter the attemp
            data = sorted(g, key=lambda x: x.timeStamp)[attemp] # filter the attemp

            keys = len(data.data) # 
            interactions = (keys-5)/8  # 5 is evaluation data and 8 is the key of one interaction
            for e in range(interactions):
                if data.data['question.%s.id'%e] == qid:
                    result = data.data['question.%s.result'%e]
                    if result:
                        correct.append(userid)
                    else:
                        incorrect.append(userid)
                    break

        return (correct,incorrect)

    
    def getQuestionTitle(self, qid):
        return self._getOb(qid).Title()

    ########
    #  Module dependency
    ########        

    def passEvaluation(self, userId=None):
        taskId = self.getId()

        if not userId:
            userId = self.AuthenticatedMember()

        track = self.track.getLastUserTrack(taskId,0,userId)
        if track:
            score = track.data['evaluation.score']
            return score > self.getMinScoreGrade()
        return False


    def canTakeExam(self, userId=None):
        """
        """
        # comprobar si tiene asociado un examen

        if not userId:
            userId = self.AuthenticatedMember()

        evaluation = self.getEvaluationDependecy()
        if evaluation:
            return evaluation.passEvaluation(userId)
        return True

    def getPublishState(self):
        """
        """
        wftool = getToolByName(self, "portal_workflow")
        return wftool.getInfoFor(self, 'review_state')
