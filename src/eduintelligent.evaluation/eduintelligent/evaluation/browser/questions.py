"""Define a browser view for the Exam content type. In the FTI 
configured in profiles/default/types/*.xml, this is being set as the default
view of that content type.
"""
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from plone.memoize.instance import memoize


class QuestionChoiceView(BrowserView):
    """Default view of a course
    """    
    __call__ = ViewPageTemplateFile('templates/questionchoice.pt')
    
class QuestionFillInView(BrowserView):
    """Default view of a course
    """    
    __call__ = ViewPageTemplateFile('templates/questionfillin.pt')

