from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.component import getUtility

from AccessControl import getSecurityManager, Unauthorized
from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ModifyPortalContent
from Products.statusmessages.interfaces import IStatusMessage
from plone.memoize.instance import memoize

from eduintelligent.edutrainingcenter.config import SUBGROUPS


class SubgroupsView(BrowserView):
    """ A course listing view for a division """

    template = ViewPageTemplateFile('templates/subgroups.pt')
    
    def __call__(self):
        form = self.request.form
        if 'form.button.Update' in form:
            self._update_subgroup()
            IStatusMessage(self.request).addStatusMessage(u"Changes saved.", type='info')
        elif 'form.button.AddGroup' in form:
            try:
                self._add_subgroup()
            except ValueError, e:
                IStatusMessage(self.request).addStatusMessage(e.args[0], type='error')
            else:
                IStatusMessage(self.request).addStatusMessage(u"Subgroup added.", type='info')
        
                # Clear the request so that the next item we add doesn't have
                # ghost values
                form['title'] = None
                form['description'] = None

        return self.template()
    

    @memoize
    def _update_subgroup(self):
        pass
        
    @memoize    
    def _add_subgroup(self):
        request = self.request
        form = request.form

        title = form.get('title', None)
        description = form.get('description', "")
        prefix = form.get('prefix', "")

        # Remove the in-field labels if they were submitted
        if title == "Title":
            title = ""
        if description == "Group description":
            description = ""

        if not title or not description:
            raise ValueError(u"You must provide a title and description")
        if not prefix:
            raise ValueError(u"You must select a group")

        parent = self.context.getGroupId()

        tctool = getToolByName(self.context, 'portal_tctool')
        group = tctool.addGroup(parent=parent, prefix=prefix, name=title, description=description)

        return group

    @memoize    
    def getSubgroups(self):
        """
        """
        parent = self.context.getGroupId()
        tctool = getToolByName(self.context, 'portal_tctool')
        
        listsg = []

        for sg in SUBGROUPS.items():
            grps = tctool.getGroups(parent=parent, prefix=sg[0])
            sub = {}
            sub['id']= sg[0]
            sub['title']= sg[1]
            sub['content'] = grps
            listsg.append(sub)
        return listsg

