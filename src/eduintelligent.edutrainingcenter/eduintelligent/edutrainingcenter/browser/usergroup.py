from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from AccessControl import getSecurityManager, Unauthorized
from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ModifyPortalContent
from Products.statusmessages.interfaces import IStatusMessage

from plone.i18n.normalizer.interfaces import IUserPreferredURLNormalizer
from plone.memoize.instance import memoize

#from zope.component import getUtility

class UserGroupView(BrowserView):
    """ A course listing view for a division """

    template = ViewPageTemplateFile('templates/usergroup.pt')
    
    def __call__(self):
        form = self.request.form
        if 'form.button.Edit' in form:
            self._delete_from_group()
            IStatusMessage(self.request).addStatusMessage(u"Changes saved.", type='info')
        elif 'form.button.Add' in form:
            try:
                self._add_to_group()
            except ValueError, e:
                IStatusMessage(self.request).addStatusMessage(e.args[0], type='error')
            else:
                IStatusMessage(self.request).addStatusMessage(u"User added.", type='info')
        
        #elif 'form.button.Search' in form:
        #    self.user_search_results()
        

        return self.template()

    @memoize
    def _delete_from_group(self):
        context = aq_inner(self.context)
        request = self.request
        form = request.form
    
        delete = form.get('delete', [])
        group = form.get('groupname', '')
        print "DELETE: ",delete, 'GROUP', group
        
        tctool = getToolByName(self.context, 'portal_tctool')
        tctool.removeUserGroup(users=delete, group=group)

        
    @memoize    
    def _add_to_group(self):
        context = aq_inner(self.context)
        request = self.request
        form = request.form
    
        add = form.get('add', [])
        group = form.get('groupname', '')        
        print "ADD: ", add, 'GROUP', group
        
        tctool = getToolByName(self.context, 'portal_tctool')
        tctool.addUserGroup(users=add, group=group)
    

    @memoize
    def usersingroup(self):
        """Return the users from a group
        """
        parent = self.context.getGroupId()
                
        tctool = getToolByName(self.context, 'portal_tctool')
        groups = tctool.getGroups(parent=parent, prefix='group')
        
        return groups
        
    @memoize
    def user_search_results(self):
        """Return search results for a query to add new users

        Returns a list of dicts, as per role_settings()
        """
        search_term = self.request.form.get('searchstring', None)
        result = []
        if search_term:
            context = aq_inner(self.context)
            pc = getToolByName(context,'portal_catalog')
            path = '/'.join(context.getPhysicalPath())
            
            result = pc.searchResults(path=path, portal_type={ 'query' : ['eduMember']},SearchableText=search_term)
            result = [b.getObject() for b in result]
        return result
        
    @memoize
    def usersingroup(self):
        """Return the users from a group
        """
        parent = self.context.getGroupId()
                
        tctool = getToolByName(self.context, 'portal_tctool')
        groups = tctool.getGroups(parent=parent, prefix='group')
        
        return groups
        
