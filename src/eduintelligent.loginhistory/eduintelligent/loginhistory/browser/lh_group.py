#-*- coding: utf-8 -*-

from datetime import datetime

from zope.component import getUtility

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from plone.memoize.instance import memoize

from eduintelligent.loginhistory.interfaces import ILoginHistoryManager
from eduintelligent.loginhistory import loginhistoryMessageFactory as _
from eduintelligent.loginhistory.dbclasses import *

from DateTime import DateTime
import csv, time 
from cStringIO import StringIO

#from itertools import groupby

# replace by: form itertools import groupby
class groupby(dict):
    def __init__(self, seq, key=lambda x:x):
        for value in seq:
            k = key(value)
            self.setdefault(k, []).append(value)
    __iter__ = dict.iteritems


class LHGroupView(BrowserView):
    """
    """

    template = ViewPageTemplateFile('history_by_group.pt')

    def __call__(self):
        form = self.request.form
        if 'form.button.Export' in form:
            #return self.exportLoginHistory()
            return self.export_csv()

        return self.template()
    
    def getLoginFiltered(self):
        """
        """            
        lh = getUtility(ILoginHistoryManager)
        
        startdate = datetime.fromtimestamp(DateTime(self.startDate()).timeTime())
        enddate = datetime.fromtimestamp(DateTime(self.endDate()).timeTime())
        group = self.context.getGroupId()
        
        results = []
        #print lh.login_by_group_grouped(group, startdate, enddate)
        for username, g in groupby(lh.login_by_group_grouped(group, startdate, enddate), key=lambda r: r.username):
            total = len(g)
            track = sorted(g, key=lambda x: x.startdate)[-1]
            start = track.startdate
            end   = track.enddate
            ip    = track.ip
            browser = track.browser
            results.append((username, start, end, total, ip, browser))
        return results
        
    #@property
    def startDate(self):
        form = self.request.form
        sD = form.get('startDate', (DateTime()-31).strftime('%Y-%m-%d %H:%M:%S'))
        return sD
        
    #@property    
    def endDate(self):
        form = self.request.form
        eD = form.get('endDate', DateTime().strftime('%Y-%m-%d %H:%M:%S'))
        return eD
        
    def getMemerObj(self, userid):
        """
        """
        portal_membership = getToolByName(self.context, 'portal_membership')

        member = portal_membership.getMemberById(userid)
        
        # Hack temporal que corrige error cuando un usuario es eliminado
        if not member:
            class Member:
                def getFullname(self):
                    return '--'
                def getPositionName(self):
                    return '--'
                def getPlace(self):
                    return '--'
                def getProductName(self):
                    return ['--',]
                def getDivisionName(self):
                    return ['--',]
                def getDistrict(self):
                    return '--'
                def getRegion(self):
                    return '--'
                def getState(self):
                    return '--'
                def getCity(self):
                    return '--'
            member = Member()
                
        return member
        
        
    def calculateTime(self, a, b):
        """
        """
        return str(b - a).split('.')[0]
                
    def getUserLoginFiltered(self):
        """
        """            
        lh = getUtility(ILoginHistoryManager)
        form = self.request.form

        startdate = datetime.fromtimestamp(DateTime(self.startDate()).timeTime())
        enddate = datetime.fromtimestamp(DateTime(self.endDate()).timeTime())
        username = form.get('username','--')
        return lh.login_by_user(username, startdate, enddate)
        
        
    def export_csv(self):
        """
        Do a CSV export from a Python list
        """
        startdate = datetime.fromtimestamp(DateTime(self.startDate()).timeTime())
        enddate = datetime.fromtimestamp(DateTime(self.endDate()).timeTime())
        group = self.context.getGroupId()
        results = self.getLoginFiltered()
        
        buffer = StringIO()
        writer = csv.writer(buffer, quoting = csv.QUOTE_ALL)
        
        ##### Header
        
        writer.writerow(['REPORTE DE CONECTIVIDAD DE '+ group.upper(),])
        writer.writerow(['FECHA INICIO', startdate.strftime('%d/%m/%Y - %H:%M'), 'FECHA FIN', enddate.strftime('%d/%m/%Y - %H:%M')])
        writer.writerow(['Usuario','Nombre','UltimoAcceso','Total','Estado','Ciudad','Division','Distrito','Region','IP','Navegador'])
        
            
        for row in results:
            user = self.getMemerObj(row[0])
            
            writer.writerow([str(row[0]),
                    user.getFullname(),
                    row[1].strftime('%d/%m/%Y - %H:%M'),
                    str(row[3]),
                    user.getState(),
                    user.getCity(),
                    ','.join(user.getDivisionName()),
                    user.getDistrict(),
                    user.getRegion(),
		    row[4],
		    row[5],
            ])

    
        value = buffer.getvalue()
        value = unicode(value, "utf-8").encode("iso-8859-1", "replace")
        
        filename = group + '_historial'
        
        response = self.request.response
        response.setHeader('Content-Type', 'text/csv')
        response.setHeader('Content-Disposition', 'attachment;filename=%s-%s.csv' % (filename, time.strftime("%Y%m%d-%H%M")))
        return value
        
class LHUserView(BrowserView):
    """
    """
    def getUserLoginFiltered(self):
        """
        """            
        lh = getUtility(ILoginHistoryManager)
        form = self.request.form

        startdate = datetime.fromtimestamp(DateTime(self.startDate()).timeTime())
        enddate = datetime.fromtimestamp(DateTime(self.endDate()).timeTime())
        username = form.get('username','--')
        return lh.login_by_user(username, startdate, enddate)

    #@property
    def startDate(self):
        form = self.request.form
        sD = form.get('startDate', (DateTime()-31).strftime('%Y-%m-%d %H:%M:%S'))
        return sD
        
    #@property    
    def endDate(self):
        form = self.request.form
        eD = form.get('endDate', DateTime().strftime('%Y-%m-%d %H:%M:%S'))
        return eD
        
    def getMemerObj(self, userid):
        """
        """
        portal_membership = getToolByName(self.context, 'portal_membership')

        member = portal_membership.getMemberById(userid)
        
        # Hack temporal que corrige error cuando un usuario es eliminado
        if not member:
            class Member:
                def getFullname(self):
                    return '--'
                def getPositionName(self):
                    return '--'
                def getPlace(self):
                    return '--'
                def getProductName(self):
                    return ['--',]
                def getDivisionName(self):
                    return ['--',]
                def getDistrict(self):
                    return '--'
                def getRegion(self):
                    return '--'
                
            member = Member()
                
        return member
        
        
    def calculateTime(self, a, b):
        """
        """
        return str(b - a).split('.')[0]
        
