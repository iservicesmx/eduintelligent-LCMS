"""
"""
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

from eduintelligent.evaluation import evaluationMessageFactory as _

from plone.memoize.instance import memoize


class ExamDelete(BrowserView):
    """
    """    
    def __call__(self):
        form = self.request.form
        userid = form.get('userid',None)
        numeval = form.get('numeval',None)
        
        if userid and not numeval:
            for track in self.context.getDataEvaluations(userid):
                self.context.track.removeTrack(track)
                IStatusMessage(self.request).addStatusMessage(_(u"The data user has been deleted"), type='info')
        elif userid and numeval:
            num = int(numeval) - 1
            track = self.context.getDataEvaluations(userid)[num]
            self.context.track.removeTrack(track)
            IStatusMessage(self.request).addStatusMessage(_(u"The evaluation user has been deleted"), type='info')
        
        url = self.context.absolute_url() + '/@@results'
        return self.request.response.redirect(url)
    