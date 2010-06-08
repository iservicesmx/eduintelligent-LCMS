"""A standalone page showing screenings of a particular film at a particular
cinema. This view is registered for ICinema, and takes the film as a request
parameter.
"""
import types
from smtplib import SMTPAuthenticationError

from zope.component import getUtility, queryUtility, getMultiAdapter

from Acquisition import aq_inner
from AccessControl import getSecurityManager

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

from plone.memoize.instance import memoize

from eduintelligent.messages.interfaces import IMessagesManager
from eduintelligent.messages import messagesMessageFactory as _
from eduintelligent.messages import logger

MESSAGE_TEMPLATE = _(u"""\

Acaban de enviarle un mensaje personal de parte de %(name)s <%(email)s> 
para recuperarlo debe ir a: http://iservices.com.mx/

IMPORTANTE: Recuerde, esto es solamente una notificacion. Por favor, no respondas a este e-mail. 

""")


class MessagesView(BrowserView):
    """
    """
    
    template = ViewPageTemplateFile('templates/messages.pt')
    
    def __call__(self):
        form = self.request.form
        if 'form.button.New' in form:
            url = self.context.absolute_url() + '/@@message_new'
            self.request.response.redirect(url)
            
        elif 'form.button.Reply' in form:
            entries = form.get('entries', [])
            if not entries:
                IStatusMessage(self.request).addStatusMessage(_('Choose one message'), type='error')
            elif len(entries) > 1:
                IStatusMessage(self.request).addStatusMessage(_('Choose only one message'), type='error')
            else:
                url = self.context.absolute_url() + '/@@message_new?id=' + str(entries[0])
                self.request.response.redirect(url)
        elif 'form.button.Delete' in form:
            entries = form.get('entries', [])
            try:
                self.delete()
            except ValueError, e:
                IStatusMessage(self.request).addStatusMessage(e.args[0], type='error')
            else:
                IStatusMessage(self.request).addStatusMessage(_(u"%s Message(s) delete"%(len(entries))), type='info')
                url = self.context.absolute_url() + '/@@messages'
                return self.request.response.redirect(url)

        return self.template()
    
    def delete(self):
        form = self.request.form
        entries = form.get('entries', [])
        if not entries:
            raise ValueError(_(u"You must select at least one message"))
            
        manager = getUtility(IMessagesManager)    
        for msg in entries:
            manager.message_delete(msg)
        
    
    @memoize
    def messages_content(self):
        form = self.request.form
        mtool = getToolByName(self.context, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        
        category_id = form.get('category_id', 1)
        user_id = form.get('user_id', member.getId())
        
        manager = getUtility(IMessagesManager)
        
        return manager.messages_category_user(category_id, user_id)
            
    def localize(self, time):
        return self._time_localizer()(time.isoformat(), 
                                        long_format=True, 
                                        context=aq_inner(self.context),
                                        domain='plonelocales')

    @memoize
    def _time_localizer(self):
        context = aq_inner(self.context)
        translation_service = getToolByName(context, 'translation_service')
        return translation_service.ulocalized_time
        
    def getFullname(self, userid):
        if userid.startswith('g:'):
            pg = getToolByName(self.context, 'portal_groups')
            group = pg.getGroupById(userid[2:])
            if group:
                return group.getGroupTitleOrName()
        else:
            membership = getToolByName(self.context, 'portal_membership')
            member = membership.getMemberById(userid)
            if member:
                name = member.getProperty('fullname',userid)
                return name
        
        
class MessageView(BrowserView):
    """List screenings of a film at a cinema
    """

    template = ViewPageTemplateFile('templates/message_view.pt')

    def __call__(self):
        form = self.request.form
        if 'form.button.New' in form:
            url = self.context.absolute_url() + '/@@message_new'
            self.request.response.redirect(url)

        elif 'form.button.Reply' in form:
            entries = form.get('id', None)
            if not entries:
                IStatusMessage(self.request).addStatusMessage(_("There isn't message"), type='error')
            else:
                url = self.context.absolute_url() + '/@@message_new?id=' + str(entries)
                self.request.response.redirect(url)
        elif 'form.button.Delete' in form:
            try:
                self.delete()
            except ValueError, e:
                IStatusMessage(self.request).addStatusMessage(e.args[0], type='error')
            else:
                IStatusMessage(self.request).addStatusMessage(_(u"Message(s) delete"), type='info')
                url = self.context.absolute_url() + '/@@messages'
                return self.request.response.redirect(url)
                
        elif 'form.button.Cancel' in form:
            url = self.context.absolute_url() + '/@@messages'
            self.request.response.redirect(url)
            

        return self.template()
        
    def delete(self):
        form = self.request.form
        entries = form.get('id', None)
        
        manager = getUtility(IMessagesManager)
        manager.message_delete(entries)
        
        
    def message(self):
        form = self.request.form
        entries = form.get('id', None)
        if not entries:
            raise ValueError(_(u"There isn't message"))
            
        read_flag = form.get('read_flag', False)
        manager = getUtility(IMessagesManager)            
        return manager.message_by_id(entries, read_flag)

    def getFullname(self, userid):
        if userid.startswith('g:'):
            pg = getToolByName(self.context, 'portal_groups')
            group = pg.getGroupById(userid[2:])
            if group:
                return group.getGroupTitleOrName()
        else:
            membership = getToolByName(self.context, 'portal_membership')
            member = membership.getMemberById(userid)
            if member:
                name = member.getProperty('fullname',userid)
                return name
        

class MessageNew(BrowserView):
    """
    """

    template = ViewPageTemplateFile('templates/message_new.pt')
    
	
    def __init__(self, context, request):
        super(MessageNew, self).__init__(context, request)
        self.membership = getToolByName(context, 'portal_membership')

        self.mailhost = getToolByName(context, 'MailHost')
       
        self.urltool = getToolByName(context, 'portal_url')
    
        self.portal = self.urltool.getPortalObject()
        self.email_charset = self.portal.getProperty('email_charset')
        self.portal_title = self.portal.getProperty('title')
        self.portal_email = self.portal.getProperty('email_from_address')
    

    def __call__(self):
        form = self.request.form
        if 'form.button.Send' in form:
            try:
                self.send()
                IStatusMessage(self.request).addStatusMessage(_(u"Message has been sent"), type='info')
                url = self.context.absolute_url() + '/@@messages'
                self.request.response.redirect(url)
    	        
            except ValueError, e:
                IStatusMessage(self.request).addStatusMessage(e.args[0], type='error')
                            

        elif 'form.button.Cancel' in form:
            IStatusMessage(self.request).addStatusMessage(_(u"Message has been canceled"), type='info')
            url = self.context.absolute_url() + '/@@messages'
            self.request.response.redirect(url)
            

        return self.template()

    def reply_fill(self):
        form = self.request.form
        entries = form.get('id', None)
        if entries:
            manager = getUtility(IMessagesManager)
            return manager.message_by_id(entries, read_flag=False)
        return None

        
    def send(self):
        """
        """
        pg = getToolByName(self.context, 'portal_groups')
        membership = getToolByName(self.context, 'portal_membership')        
                        
        form = self.request.form
        user_list = form.get('user_list', [])
        if not user_list:
            raise ValueError(_(u"You must select at least one recipient"))
        
        subject = form.get('subject', None)
        if not subject:
            raise ValueError(_(u"The message has not subject"))
        
        body = form.get('body', '')
        category = form.get('category_id', 1)
        
        sender = membership.getAuthenticatedMember()
        fullname = sender.getProperty('fullname')
        senderId = sender.getId()
        manager = getUtility(IMessagesManager)
        
        data_sender = dict(name = fullname or senderId,
                    email = sender.getProperty('email', None)
                )
        
        
        for receiver in user_list:
            if receiver.startswith('g:'):
                logger.info("is a Group")
                group = pg.getGroupById(receiver[2:])
                if group:
                    members = group.getGroupMembers()
                    logger.info("have %s members" %(len(members)))
                    for member in members:
                        email = member.getProperty('email', None)
                        #brincar mensaje para uno mismo                            
                        manager.message_new(int(category), 
                                            senderId, 
                                            member.getId(), 
                                            subject, body)
                        logger.info("Message DB for %s"%(member.getId()))
                        if email:
                            try:
                                self.send_email(data_sender, email)
                                logger.info("Message E-Mail for %s"%(member.getId()))                       
                            except SMTPAuthenticationError, inst:                        
                                logger.error("Authentication error:" + str(inst))
                                #logger.error("Error while sending email to " + email)
                            #finally:
                                raise ValueError(_(u"One or more emails could not be sent. Please try again later or contact the site Administrator"))
                        else:
                            fullname = member.getProperty('fullname', None)
                            raise ValueError (_("User %s does not have e-mail account associated"%(fullname)))
                            
                    manager.message_new(3, receiver, senderId, subject, body, read_flag=True) # copy sent
                    logger.info("copy sent")

            else:
                member = membership.getMemberById(receiver)
                email = member.getProperty('email', None)
                
                manager.message_new(int(category), sender.getId(), receiver, subject, body)
                #Make the same email on Sent items
                manager.message_new(3, receiver, sender.getId(), subject, body, read_flag=True)
                
                if email:
                    try :
                        self.send_email(data_sender, email)
                    except SMTPAuthenticationError, inst:                        
                        logger.error("Authentication error:" + str(inst))
                        logger.error("Error while sending email to " + email)
                    #finally:
                        raise ValueError (_(u"The mail could not be sent. Please try again later"))
                
        #return True
    #@memoize    
    def send_email(self, data, email):
        """Send the email to the user and redirect to the
        front page, showing a status message to say the message was received.
        """

        #context = aq_inner(self.context)

        #mailhost = getToolByName(context, 'MailHost')
        #urltool = getToolByName(context, 'portal_url')
        
        #portal = urltool.getPortalObject()
        #email_charset = portal.getProperty('email_charset')
        #title = portal.getProperty('title')
        # Construct and send a message
        source = "%s <%s>" % (self.portal_title, self.portal_email)
        subject = _('Nuevo mensaje en') + " " + self.portal_title  
        message = MESSAGE_TEMPLATE % data
	
	self.mailhost.secureSend(message, email, str(source),
                            subject=subject, subtype='plain',
                            charset=self.email_charset, debug=False,
                            From=source)


        #return ''    
        
    def getFullname(self, userid):
        if userid.startswith('g:'):
            pg = getToolByName(self.context, 'portal_groups')
            group = pg.getGroupById(userid[2:])
            if group:
                return group.getGroupTitleOrName()
        else:
            membership = getToolByName(self.context, 'portal_membership')
            member = membership.getMemberById(userid)
            if member:
                name = member.getProperty('fullname',userid)
                return name
        

class MessageSearchUser(BrowserView):
    """
    """

    template = ViewPageTemplateFile('templates/message_searchuser.pt')

    def __call__(self):
        form = self.request.form
        if 'form.button.Send' in form:
            pass

        elif 'form.button.Cancel' in form:
            pass

        return self.template()
        
    def getPrincipalGroups(self):
        """
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        
        return [ dict(id=content.getId,
                      title=content.Title,)
                 for content in catalog(meta_type='TrainingCenter',
                                             sort_on='sortable_title')
               ]
        
    def getUserMainGroup(self):
        context = aq_inner(self.context)
        membership = getToolByName(context, 'portal_membership')
        member = membership.getAuthenticatedMember()
        #Ojo: Se asume que los usuarios que no tienen main_group
        #van a ser manager (Admin, por ejemplo)
        main_group = member.getProperty('main_group', 'manager')
        return main_group

    def getGroups(self):
        """Return the groups.
        """         
        filter = self._allocateFilter()

        # TODO: alter grouptool with pas.
        grouptool = getToolByName(self.context, 'portal_groups')
        groups = grouptool.listGroups()

        ret = []
        for group in groups:
            gid = group.getId()
            if not self._groupIdFilterMatch(gid, filter):
                continue

            ret.append((gid, group.getGroupTitleOrName()))

        return ret
        
    def isSelected(self, param, value):
        param = self.request.get(param)
        if param:
            if param is types.StringType:
                param = [param]
            if value in param:
                return True
        return False
        
    def isManager(self):
        root = aq_inner(self.context)
        is_manager = getSecurityManager().checkPermission('Manage portal', root)
        return is_manager

    def getUsersSerached(self):
        """
        """
        context = aq_inner(self.context)
        acl_users = getToolByName(context, 'acl_users')
        
        info = []
        form = self.request.form
        if 'form.button.SearchUser' in form:
            search_term = form.get('searchabletext', None)
            if not search_term:
                return []
        
            hunter = getMultiAdapter((context, self.request), name='pas_search')
            for userinfo in hunter.searchUsers(fullname=search_term):
                userid = userinfo['userid']

                user = acl_users.getUserById(userid)
                info.append(dict(id    = userid,
                                 fullname = user.getProperty('fullname') or user.getId() or userid,
                                 main_group = user.getProperty('main_group', None)
                                 )
                            )
        
        elif 'form.button.SearchGroup' in form:
            groups = form.get('selectgroup', [])
            for group in groups:
                pg = getToolByName(self.context, 'portal_groups')
                group = pg.getGroupById(group)
                if group:
                    members = group.getGroupMembers()
                    
                    for member in group.getGroupMembers():
                        info.append(dict(id    = member.getId(),
                                         fullname = member.getProperty('fullname', None) or member.getId(),
                                         main_group = member.getProperty('main_group', None)
                                         )
                                    )
                    
        return info
    

    def _allocateFilter(self):
        ##  obtener grupo

        form = self.request.form
    
        group = form.get('cecap', None)
        
        #if not group == '*'
        #if group <> '*'
        #if group != '*'
        #if not group is '*'
        if not group:
            group = self.getUserMainGroup()
        group += '*'
        return [group,]
                
    def _groupIdFilterMatch(self, gid, filter):
        """Check if gid matches filter.
        """
        for fil in filter:
            print fil
            # wildcard match
            if fil.find('*') != -1:

                # all groups are affected
                if fil == '*':
                    return True

                # wildcard matches like '*foo'
                elif fil.startswith('*'):
                    if gid.endswith(fil[1:]):
                        return True

                # wildcard matches like 'foo*'
                elif fil.endswith('*'):
                    if gid.startswith(fil[:-1]):
                        return True

                # wildacard matches like '*foo*'
                else:
                    if gid.find(fil[1:-1]) != -1:
                        return True

            # exact match
            else:
                if fil == gid:
                    return True

        return False
