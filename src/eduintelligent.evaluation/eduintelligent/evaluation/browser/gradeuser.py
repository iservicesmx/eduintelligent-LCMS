"""
"""
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from eduintelligent.evaluation import evaluationMessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage

from plone.memoize.instance import memoize
from eduintelligent.evaluation import logger

class GradeUser(BrowserView):
    """
    """    
    def __call__(self):
        form = self.request.form
        userid = form.get('userid',None)
        
        prefix = 'question.'
        interactions = [i for i in form.keys() if i.startswith(prefix)]
        
        tmp = {}
        for key in interactions:
            tmp[key] = form[key]
            
        evaluation = self.context.getLastEvaluation(userid)
        evaluation.update(tmp)
        
        if 'grade' in form: 
            evaluation['evaluation.score'] = self.context.calculateScore(evaluation)
            evaluation['evaluation.scored'] = 1
            self.context.saveUserResponse(evaluation, userId=userid)
            self.context.sendMessage(evaluation, userId=userid)
            self.context.setScoreKardex(evaluation, userId=userid)
            IStatusMessage(self.request).addStatusMessage(_(u"The user has been graded with ") + str(evaluation['evaluation.score']), type='info')
            
        elif 'save' in form:
            self.context.saveUserResponse(evaluation, userId=userid)
            IStatusMessage(self.request).addStatusMessage(_(u"The exam has been saved for further review"), type='info')
        
        url = self.context.absolute_url() + '/@@grade'
        return self.request.response.redirect(url)
        