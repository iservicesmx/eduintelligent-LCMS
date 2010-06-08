"""Define a browser view for the SCO content type. In the FTI 
configured in profiles/default/types/*.xml, this is being set as the default
view of that content type.
"""

from Acquisition import aq_inner

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from plone.memoize.instance import memoize

from eduintelligent.sco.scorm.interfaces import IScormAPI
from eduintelligent.sco.scorm.tracking import timeStamp2ISO

class ScormIO(BrowserView):
    template = ViewPageTemplateFile('templates/scorm_io.pt')
    
    def __call__(self):
        form = self.request.form
        
        traduct = {}
        traduct["cmi_lesson_status"] = 'cmi.core.lesson_status'
        traduct["cmi_lesson_location"] = 'cmi.core.lesson_location'
        traduct["cmi_credit"] = 'cmi.core.credit'
        traduct["cmi_entry"] = 'cmi.core.entry'
        traduct["cmi_raw"] = 'cmi.core.score.raw'
        traduct["cmi_total_time"] = 'cmi.core.total_time'
        traduct["cmi_session_time"] = 'cmi.core.session_time'
        traduct["cmi_suspend_data"] = 'cmi.suspend_data'
        traduct["cmi_scoreMin"] = 'cmi.core.score.min'
        traduct["cmi_scoreMax"] = 'cmi.core.score.max'
        
        cmi={}
        for k in self.request.keys():
            if k.startswith('cmi_'):
                value = self.request[k]
                #if value is [] then get the first element
                cmi[traduct[k]] = value
                
        item = self.request.get('item',None)
        if cmi:
            # print "item",item
            # print "cmi",cmi
            self.context.saveToUserTrack(cmi, memberId=None, item=item)
        
        return self.template()

class ScormView(BrowserView):
    """Default view of a course
    """
    #__call__ = ViewPageTemplateFile('templates/scorm.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.track = self.context.track
        self.scormAPI = IScormAPI(self.track)
        
    # statistics
    
    def getModuleReport(self, item=None):
        portal_membership = getToolByName(self, 'portal_membership')
        
        report = []
        users = self.track.getUserNames(item)
        for user in users:
            data = {}
            member = portal_membership.getMemberById(user)
            memberId = member.getId()
            memberName = member.getProperty('fullname')
            data['id'] = memberId
            data['name'] = memberName
            
            scorm = self.track.getLastUserTrack(item,0,memberId).data
            
            data['total_time'] = scorm['cmi.core.total_time']
            data['session_time'] = scorm['cmi.core.session_time'] 
            data['lesson_status'] = scorm['cmi.core.lesson_status']
            data['score_raw'] = scorm['cmi.core.score.raw']
            
            report.append(data)
            
        return report
            

    def getRanking(self, assessmentId, runId=-1, maxCount=-1):
        """ """
        result = self.track.scormStats.getRanking(assessmentId, int(runId))
        maxCount = int(maxCount)
        if maxCount > 0:
            result = result[:maxCount]
        return result

    def getTotals(self):
        """ """
        return self.track.scormStats.getTotals()

    def getUserTotal(self, userName):
        """ """
        return self.track.scormStats.getUserTotal(userName)

    def getQuestionTotals(self):
        """ """
        return self.track.scormStats.getQuestionTotals()

    def getTopicTotals(self):
        """ """
        return self.track.scormStats.getTopicTotals()

