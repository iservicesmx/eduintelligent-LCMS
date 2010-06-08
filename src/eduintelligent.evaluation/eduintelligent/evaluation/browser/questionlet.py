from zope.interface import implements, alsoProvides
from zope.component import getMultiAdapter

from zope.viewlet.interfaces import IViewlet
from zope.viewlet.interfaces import IViewletManager

from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from eduintelligent.evaluation import logger
from eduintelligent.evaluation.interfaces import IBannerProvider

class QuestionViewlet(BrowserView):
    """Viewlet
    """
    implements(IViewlet)
    
    choice = ViewPageTemplateFile('templates/viewchoice.pt')
    fillin = ViewPageTemplateFile('templates/viewfillin.pt')
        
    def __init__(self, context, request, view, manager):
        super(QuestionViewlet, self).__init__(context, request)
        self.__parent__ = view
        self.view = view
        self.manager = manager
        self.type = None
        self.specs = {}
        
    def update(self):
        
        self.specs = {}
        interaction, obj = self.view.getQuestion()
        self.specs['interaction'] = interaction
        self.specs['qid'] = obj.getId()
        self.specs['question'] = obj.Title()
        self.type = self.specs['type'] =  obj.getTypeQuestion()
        self.specs['seconds'] = obj.getMaxTimeResponseQuestion()
        self.specs['weighting'] = obj.getWeighting()
	self.specs['haveimage'] = obj.getQimage()
	self.specs['image']=obj.tag(scale='preview')
	if self.type == 'choice':
            self.specs['button'] = obj.getTypeInput()
            self.specs['answers'] = obj.getAnswersOrdered()
            self.render = self.choice
        elif self.type == 'fill-in':
            self.render = self.fillin
        elif self.type == 'true-false':
            pass
        elif self.type == 'matching':
            pass
        elif self.type == 'sequencing':
            pass
        elif self.type == 'numeric':
            pass
        
    def isLast(self, interaction):
        """"""
        if interaction + 1 == self.context.getNumberUserQuestion():
            return True
        return False

    def qimage(self):
	context = aq_inner(self.context)
	return context.getQimage(scale='preview')
	    