"""Define a browser view for the Lessons content type. In the FTI 
configured in profiles/default/types/*.xml, this is being set as the default
view of that content type.
"""
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from plone.memoize.instance import memoize


class LessonsView(BrowserView):
    """Default view of a course
    """    
    __call__ = ViewPageTemplateFile('templates/lessons.pt')
    
    #
    # cuidado, el módulo que tenga el exámen de referencia vacio, debe ser visible
    #   ""     el examen debe tener dependencia de otro examen
    #
    @memoize
    def full_contents(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        
        contents = [ content for content in catalog(path=dict(query='/'.join(context.getPhysicalPath()),
                                      depth=1),
                                      sort_on='sortable_title',) ]
        tmp_list = []
        for content in contents:
            tmp = dict(url=content.getURL(),
                        title=content.Title,
                        description=content.Description,
                        view=True,)
            
            if content.portal_type == 'PloneArticleMultiPage':
                content = content.getObject()
                tmp['view'] = content.canViewModule()
                
            tmp_list.append(tmp)
            
        return tmp_list
    
        
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
