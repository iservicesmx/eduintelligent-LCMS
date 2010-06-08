"""Define a browser view for the Quiz content type. In the FTI 
configured in profiles/default/types/*.xml, this is being set as the default
view of that content type.
"""
import random
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from plone.memoize.instance import memoize


class QuizView(BrowserView):
    """Default view of a quiz
    """    
    
    template = ViewPageTemplateFile('templates/quiz_resolve.pt')
    results = ViewPageTemplateFile('templates/quiz_results.pt')
    
    def __call__(self):
        form = self.request.form
        if 'form.button.Next' in form:
            self.next()
            return self.template()
        elif 'form.button.Finish' in form:
            self.next()
            return self.results()
        ## cuando se llena debe de rellenar con la pregunta    
        return self.template()
    
    @memoize
    def next(self):
        # obtiene el form
        # convierte los datos del form a claves scorm
        # actualiza la bd
        pass

    

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
    

    def getNumberUserQuestion(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')

        questions = context.getNumberOfRandomQuestions()

        if questions > 0:
            return questions

        return len(catalog(path=dict(query='/'.join(context.getPhysicalPath()), depth=1),))
    