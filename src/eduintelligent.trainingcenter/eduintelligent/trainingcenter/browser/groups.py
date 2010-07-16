from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from AccessControl import getSecurityManager, Unauthorized
from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ModifyPortalContent
from Products.statusmessages.interfaces import IStatusMessage

from plone.memoize.instance import memoize

class GroupsView(BrowserView):
    """ A course listing view for a division """

    template = ViewPageTemplateFile('templates/groups.pt')
    
    def __call__(self):
        form = self.request.form
        if 'form.button.Update' in form:
            self._update_group()
            IStatusMessage(self.request).addStatusMessage(u"Changes saved.", type='info')
        elif 'form.button.AddGroup' in form:
            try:
                self._add_group()
            except ValueError, e:
                IStatusMessage(self.request).addStatusMessage(e.args[0], type='error')
            else:
                IStatusMessage(self.request).addStatusMessage(u"Group added.", type='info')
        
                # Clear the request so that the next item we add doesn't have
                # ghost values
                form['title'] = None
                form['description'] = None

        return self.template()
    
    
    @memoize
    def _update_group(self):
        pass
        
    @memoize    
    def _add_group(self):
        context = aq_inner(self.context)
        request = self.request
        form = request.form
    
        title = form.get('title', None)
        description = form.get('description', "")
    
        # Remove the in-field labels if they were submitted
        if title == "Title":
            title = ""
        if description == "Group description":
            description = ""
    
        if not title or not description:
            raise ValueError(u"You must provide a title and description")
    
            
        parent = self.context.getGroupId()
        
        tctool = getToolByName(self.context, 'portal_tctool')
        group = tctool.addGroup(parent=parent, prefix='group',name=title, description=description)
    
        return group
    @memoize
    def grps(self):
        """Return the groups of this training center
        """
        parent = self.context.getGroupId()
                
        tctool = getToolByName(self.context, 'portal_tctool')
        groups = tctool.getGroups(parent=parent, prefix='group')
        
        return groups
        
        

