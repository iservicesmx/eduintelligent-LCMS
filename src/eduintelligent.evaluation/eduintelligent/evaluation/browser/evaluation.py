"""Define a browser view for the Evaluation content type. In the FTI 
configured in profiles/default/types/*.xml, this is being set as the default
view of that content type.
"""
import time
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

from plone.memoize.instance import memoize
from eduintelligent.evaluation import logger
from eduintelligent.evaluation import evaluationMessageFactory as _

class EvaluationView(BrowserView):
    """Default view of a course
    """    
    template = ViewPageTemplateFile('templates/resolve.pt')
    results = ViewPageTemplateFile('templates/resume.pt')
    
    def __call__(self):
        form = self.request.form
        if 'Next' in form:
            answers = form.get('answers',[])
            timeout = form.get('timeout',0)
            if not answers and not timeout:
                IStatusMessage(self.request).addStatusMessage(_(u"You do not select answer"), type='error')
                return self.template()
            self.next()
            return self.template()
        elif 'Finish' in form:
            answers = form.get('answers',[])
            timeout = form.get('timeout',0)            
            if not answers and not timeout:
                IStatusMessage(self.request).addStatusMessage(_(u"You do not select answer"), type='error')
                return self.template()
            
            self.next()
            self.finish()
            return self.results()
            
        if 'Init' in form:
            return self.template()
            
        if self.isResolved():
            return self.results()
        
        ## cuando se llena debe de rellenar con la pregunta    
        return self.template()
    
    def getQuestion(self):
        data = self.context.getEvaluation()

        total = (len(data)-5)/8
        for i in range(total):
            qid = data['question.%s.id'%i]
            if data['question.%s.type'%i] == '':
                obj = self.context._getOb(qid)
                return i, obj
                
                
    def next(self):
        data = {}
        form = self.request.form
        qid = form.get('qid','')
        interaction = form.get('interaction','')
        prefix = 'question.%s.'%int(interaction)
        typ = form.get('type','')
        data[prefix + 'type'] = typ 
        data[prefix + 'weighting'] = form.get('weighting', 1.0)
        data[prefix + 'time'] = form.get('timestamp','')
        data[prefix + 'latency'] = form.get('latency','')
        if typ == 'choice':
            obj = self.context._getOb(qid)
            answers = form.get('answers',[])
            data[prefix + 'student_response'] = answers 
            data[prefix + 'result'] = obj.getResult(answers)
        elif typ == 'fill-in':
            answers = form.get('answers','')
            data[prefix + 'student_response'] = answers
            data['evaluation.open'] = 1
            
        self.context.saveUserResponse(data)
        #logger.info("next:")
        #logger.info(data)
        
    def finish(self):
        data = {}
        evaluation = self.context.getEvaluation()
        data['evaluation.end'] = time.time()
        if not evaluation['evaluation.open']:
            data['evaluation.score'] = self.context.calculateScore(evaluation)
            data['evaluation.scored'] = 1
            self.context.sendMessage(data)
            self.context.setScoreKardex(data)
        #logger.info(data)
        self.context.saveUserResponse(data)
        
    def isResolved(self):
        ## Aqui se verifica si ya paso el tiempo del examen
        ## y se califica
        
        ## ver que el examen no este calificado (abierto)
        
        evaluation = self.context.getLastEvaluation()
        if evaluation and evaluation['evaluation.end']:
            return True
                        
        #if evaluation and evaluation['evaluation.open'] and evaluation['evaluation.end']:
        #    return True
            
        return False

    
### Vista de Admin #####