"""Define a browser view for the Exam content type. In the FTI 
configured in profiles/default/types/*.xml, this is being set as the default
view of that content type.
"""
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

from plone.memoize.instance import memoize

from eduintelligent.evaluation import evaluationMessageFactory as _
from eduintelligent.evaluation.content.evaluation import groupby

class ExamView(BrowserView):
    """Default view of a course
    """    
    __call__ = ViewPageTemplateFile('templates/exam.pt')

    @memoize
    def contents(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        
        return [ dict(url=content.getURL(),
                      title=content.Title,
                      description=content.Description,)
                 for content in 
                    catalog(path=dict(query='/'.join(context.getPhysicalPath()),
                                      depth=1),
                            sort_on='sortable_title',)
               ]


class ExamResults(BrowserView):
    """View that displays the results sorted by average
    """    
    __call__ = ViewPageTemplateFile('templates/results.pt')
    sort_on='average'
    
    def rowHighlight(self,row_number):
        """
        Returns a string representig the css class depending on row number.
        Only for rows 1,2 and 3.
        """
        if row_number == 1:
            return "row-first"
        elif row_number == 2:
            return "row-second"
        elif row_number == 3:
            return "row-third"
        else:
            return ''

    def compareFunction(self,a,b):
        """
        Comparing function used to sort the results returned by self.contents
        """
        c = a[self.sort_on]
        d = b[self.sort_on]
        if c > d:
            return -1
        elif c == d:
            return 0
        else:  #c < d
            return 1
        
    def averageScores (self,score,scored,score_extra,scored_extra):
        """
        Function that calculates the average of two scores. This averaging
        changes depending on wether the user has been scored.
        
        """
        if not scored :
            return 0.0
        elif scored and not scored_extra:
            return score
        else:
            return ((score + score_extra) / 2)
    
    @memoize
    def contents(self):
        """
            Return contents, sorted by average.
        """
        context = aq_inner(self.context)
        data = []
        for taker, examresults in groupby(context.track.values(), key=lambda r: r.userName):
            #select the last exam from examresults
            e = sorted(examresults, key=lambda x: x.timeStamp)[-1].data
            
            if not e['evaluation.scored'] and e['evaluation.open']:
                continue
            
            data.append(dict (end = context.utilConvertTime(e['evaluation.end']),
                       start = context.utilConvertTime(e['evaluation.start']),
                       time = context.utilCalculeTime(e['evaluation.start'],
                                                      e['evaluation.end']),
                       score = e['evaluation.score'],
                       scored = e['evaluation.scored'],
                       score_extra = e.get('evaluation.score_extra') or 0.0,
                       scored_extra = e.get('evaluation.scored_extra') or False,
                       userid = taker,
                       member = context.AuthenticatedMemberById(taker),
                       #oportunities = ???
                       average = self.averageScores (e['evaluation.score'],e['evaluation.scored'],
                                                     e.get('evaluation.score_extra') or 0.0,
                                                     e.get('evaluation.scored_extra') or False,),
                       oportunities = len(examresults),
                       ))
        #finally sort by average    
        data.sort(cmp=self.compareFunction)
        return data
        

class ExamUpdateExtraGrade(ExamResults):
    """View for adding/updating extra grades.
    """
    template = ViewPageTemplateFile('templates/extra.pt')
    sort_on='score_extra'
    errormsg = []
    
    def __call__(self):
        self.errormsg = []
        form = self.request.form
        if 'ExamUpdateExtraGrade' in form:
            for key in form.keys():
                if key.startswith('score_extra.'):
                    #key = extra_grade.username
                    extra_grade = form[key]
                    userid = key.split('.')[-1]
                    if self.is_valid_grade(extra_grade):
                        evaluation = self.context.getLastEvaluation(userid)
                        if extra_grade == '':
                            #Delete the extra grade and disable it.
                            evaluation['evaluation.scored_extra'] = False
                            evaluation['evaluation.score_extra'] = 0.0
                        else:
                            evaluation['evaluation.scored_extra'] = True
                            evaluation['evaluation.score_extra'] = float(extra_grade)

                        self.context.saveUserResponse(evaluation, userId=userid)
                    else:
                        self.errormsg.append(userid)
        if len(self.errormsg):
            IStatusMessage(self.request).addStatusMessage(_(u"Invalid input in one or more fields. Please correct."), type='error')
        return self.template()
        
    def is_valid_grade(self,grade):
        if grade == '':
            return True
        
        cal = None
        try:
            cal = float(grade)
        except ValueError:
            return False
        
        if cal <= 0.0 or cal > 100.0:
            return False
        
        return True
    
    def has_error (self,fieldname):
        """
        If fieldname equals self.errormsg, then the fieldname has a
        validation error.
        If so returns the error classname, else, None
        """
        if fieldname in self.errormsg:
            return "errclass"
        return ""

class ExamStatistics(ExamResults):
    """View for Exam Statistics.
    """
    __call__ = ViewPageTemplateFile('templates/statistics.pt')
    sort_on='counts'
    
    def compareFunction(self,a,b):
        c = len(a[self.sort_on][1])
        d = len(b[self.sort_on][1])
        if c > d:
            return -1
        elif c == d:
            return 0
        else:  #c < d
            return 1
    
    @memoize
    def contents(self):
        """
            Return contents, only failed exams
        """
        context = aq_inner(self.context)
        
        data = context.getQuestionsStatistics()
        data.sort(cmp=self.compareFunction)
        return data

class ExamFailed(ExamResults):
    """View for Failed exams
    """
    __call__ = ViewPageTemplateFile('templates/failed.pt')
    minScoreGrade = 7.0
    
    def hasFailed(self,exam):
        """
        Determines if an exam is failed (grade is below minimum score)
        """
        if exam['average'] <= self.minScoreGrade:
            return True
        else:
            return False
         
    @memoize
    def contents(self):
        """
            Return contents, only failed exams
        """
        context = aq_inner(self.context)
        
        self.minScoreGrade= self.context.getMinScoreGrade()
        data = super(ExamFailed,self).contents()
        #data = context.getGroupDataUsers()
        
        return filter(self.hasFailed,data)
    