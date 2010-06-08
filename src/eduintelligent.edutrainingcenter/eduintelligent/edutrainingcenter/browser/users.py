from zope.component import getUtilitiesFor, queryUtility, getMultiAdapter
from zope.interface import implements

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Acquisition import aq_inner, aq_parent, aq_base
from AccessControl import Unauthorized
from zExceptions import Forbidden

from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions
from Products.CMFPlone import PloneMessageFactory as _

from plone.memoize.instance import memoize, clearafter
from kss.core.interfaces import IKSSView
from plone.app.kss.plonekssview import PloneKSSView
from plone.app.content.batching import Batch

from eduintelligent.edutrainingcenter.utils import *

class UsersView(BrowserView):
    
    template = ViewPageTemplateFile('templates/users.pt')
    batching = ViewPageTemplateFile("templates/batching.pt")
    
    def __call__(self):
        """Perform the update and redirect if necessary, or render the page
        """
                
        form = self.request.form
        submitted = form.get('form.submitted', False)
        
        if submitted:
            if not self.request.get('REQUEST_METHOD','GET') == 'POST':
                raise Forbidden
            
            
        return self.template()
            
    # View        
    
    @memoize
    def user_search_results(self):
        """Return search results for a query to add new users
        
        Returns a list of dicts, as per role_settings()
        """
        context = aq_inner(self.context)
        pc = getToolByName(context,'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        search_term = self.request.form.get('search_term', None)

        if not search_term:
            contentFilter={'path':path,'portal_type':'eduMember'}
            result = pc.queryCatalog(contentFilter)
            result = [b.getObject() for b in result]
        else:
            result = pc.searchResults(path=path, portal_type={ 'query' : ['eduMember']},SearchableText=search_term)
            result = [b.getObject() for b in result]
        return result

    @property
    @memoize
    def url(self):
        """Base url, needed by the batching template."""
        url = self.context.absolute_url() + '/@@users'
        #terms = ["%s=%s" % (key, value) for key, value in
        #         self.search_filter.items()]
        #extra = '&'.join(terms)
        return url #+ '?' + extra
        
    @property
    @memoize
    def pagenumber(self):
        """Page number for batching.
        """
        return int(self.request.get('pagenumber', 1))
        

    @property
    @memoize
    def batch(self):
        """ Batch of Realestate (brains)"""
        results = self.user_search_results()
        return Batch(items=results, pagesize=30, pagenumber=self.pagenumber, navlistsize=5)
    
        
class KSSSearchView(PloneKSSView):
    """KSS view for sharing page.
    """
    implements(IKSSView)

    template = ViewPageTemplateFile('templates/users.pt')
    macro_wrapper = ViewPageTemplateFile('templates/users_tbl_wrapper.pt')

    def updateSearchInfo(self, search_term=''):

        search = getMultiAdapter((self.context, self.request,), name="users")


        # get the table body, let it render again
        # use macro in sharing.pt for that

        # get the html from a macro
        ksscore = self.getCommandSet('core')

        the_id = 'user-search'
        macro = self.template.macros[the_id]
        res = self.macro_wrapper(the_macro=macro, instance=self.context, view=search)
        ksscore.replaceHTML(ksscore.getHtmlIdSelector(the_id), res)

        return self.render()

