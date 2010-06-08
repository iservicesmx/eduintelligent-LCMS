"""Define a browser view for the course content content type. In the FTI 
configured in profiles/default/types/*.xml, this is being set as the default
view of that content type.
"""
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from plone.memoize.instance import memoize


class ExamsView(BrowserView):
    """Default view of a course
    """    
    __call__ = ViewPageTemplateFile('templates/coursecontent.pt')
    
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

class QuizzesView(BrowserView):
    """Default view of a course
    """    
    __call__ = ViewPageTemplateFile('templates/coursecontent.pt')

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

class PollsView(BrowserView):
    """Default view of a course
    """    
    __call__ = ViewPageTemplateFile('templates/coursecontent.pt')

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

class ResourcesView(BrowserView):
    """Default view of a course
    """    
    __call__ = ViewPageTemplateFile('templates/coursecontent.pt')

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
