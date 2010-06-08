#!-*- coding: utf-8 -*-
"""Define a browser view for the Course content type. In the FTI 
configured in profiles/default/types/*.xml, this is being set as the default
view of that content type.
"""

from Acquisition import aq_inner
from DateTime import DateTime
from zope.component import getMultiAdapter

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize
from Products.statusmessages.interfaces import IStatusMessage

from eduintelligent.courses.interfaces import ICourse, IBannerProvider

class CourseView(BrowserView):
    """Default view of a course
    """    
    #__call__ = ViewPageTemplateFile('templates/course.pt')
    template = ViewPageTemplateFile('templates/course.pt')

    def __call__(self):
        """Check the vigency and redirect if necessary, or render the page
        """

        # Pendiente:
        #   Mostrar en la tabla la fecha de inicio del usuario
        #      "        "                de fin del usuario
        #      "     los dias restantes
        #  Lo mismo en la lista de inscritos


        #if self.thereisuser():
        if self.valid_vigency():
            return self.template()
        else:
            IStatusMessage(self.request).addStatusMessage(u"Lo sentimos, las fechas para iniciar el diplomado han expirado, espere la próxima convocatoria",type='info')

            portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
            url = portal_state.portal_url()
            self.request.response.redirect(url)

    @memoize
    def valid_vigency(self):
        """
        """
        self.context.initStorageUsers()
        mtool = getToolByName(self.context, 'portal_membership')
        user = mtool.getAuthenticatedMember().getId()
        date = self.context.attended_users.setdefault(user, DateTime())
        return ( DateTime() - DateTime(date) )  < self.context.vigency
        #return ( DateTime() - DateTime(date) )  < self.context.getVigencyDays()

    @memoize
    def thereisuser(self):
        mtool = getToolByName(self.context, 'portal_membership')
        user = mtool.getAuthenticatedMember().getId()
        if self.context.attended_users.has_key(user):
            return True
        return False

    @memoize
    def instructor(self):
        """
        """
        return self.context.getInstructor()

    @memoize
    def count_students(self):
        """
        """
        #return len(self.context.getAttendedStudents())
        #return len(self.context.getLocalRoles(role='Student'))
        return self.context.getRegistered()

    def banner_tag(self):
        context = aq_inner(self.context)
        banner_provider = IBannerProvider(context)
        return banner_provider.tag

class CourseAtenddedUserListView(BrowserView):
    """Default view of a course
    """    
    #__call__ = ViewPageTemplateFile('templates/attendeduserlist.pt')
    template = ViewPageTemplateFile('templates/attendeduserlist.pt')

    def __call__(self):
        """Check the vigency and redirect if necessary, or render the page
        """
        form = self.request.form
        delete = form.get('form.button.Delete', False)
        if delete:
            entries = form.get('entries', [])

            for entry in entries:
                del self.context.attended_users[entry]

            context_state = self.context.restrictedTraverse("@@plone_context_state")
            url = context_state.view_url()
            self.request.response.redirect(url)

        return self.template()

    def AuthenticatedMemberById(self, userId=None):
        portal_membership = getToolByName (self, 'portal_membership')

        if not userId:
            return portal_membership.getAuthenticatedMember()
        member = portal_membership.getMemberById(userId)
        # Hack temporal que corrige error cuando un usuario es eliminado
        if not member or userId == 'admin':
            class FakeMember:
                def getFirstName(self):
                    return '--'
                def getLastName(self):
                    return '--'
                def getDivisionName(self):
                    return ['--',]
                def getState(self):
                    return '--'
            member = FakeMember()

        return member

    @memoize
    def attendedusers(self):
        """
           El contexto es un Curso
           attended_users es un registro de Zope 
        """
        ##
        #la lista de usuarios que han entrado ya a este curso:  
        users = self.context.attended_users.items()

        portal_membership = getToolByName(self, 'portal_membership')
        final_list = []
        for user in users:
            member = self.AuthenticatedMemberById(user[0])
            final_list.append ((user[0],  
                                member.getFirstName(),  
                                member.getLastName(),  
                                member.getState(),  
                                member.getDivisionName(),  
                                user[1]))  
        return final_list


