#-*- coding: utf-8 -*-

from zope.component import getUtility

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from plone.memoize.instance import memoize

from eduintelligent.loginhistory.interfaces import ILoginHistoryManager
from eduintelligent.loginhistory import loginhistoryMessageFactory as _
from eduintelligent.loginhistory.dbclasses import *

class LoginHistoryView(BrowserView):
    """List screenings of a film at a cinema
    """

    template = ViewPageTemplateFile('loginhistory.pt')

    def __call__(self):
        # form = self.request.form
        # if 'form.button.Filter' in form:
        #     courses = form.get('userid', [])
        #     if not courses:
        #         IStatusMessage(self.request).addStatusMessage(_('No se ha seleccionado un curso'), type='error')
        #     elif not cecap:
        #         IStatusMessage(self.request).addStatusMessage(_('No se ha seleccionado un CECAP'), type='error')
        #     else:
        #         self.createCourse(course, cecap)
        # 

        return self.template()
    
    def getLoginAll(self):
        """
        """
        lh = getUtility(ILoginHistoryManager)        
        return lh.login_all()
                
    def getMemerObj(self, userid):
        """
        """
        portal_membership = getToolByName(self.context, 'portal_membership')

        member = portal_membership.getMemberById(userid)
        return member
