"""
"""
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from eduintelligent.evaluation import evaluationMessageFactory as _

from plone.memoize.instance import memoize


class ExportExam(BrowserView):
    """
    """    
    def __call__(self):
        form = self.request.form
        format = form.get('format',None)
        if format == 'csv':
            return self.export_csv()
        elif format == 'xls':
            return self.export_xls()
        
        return self.export_csv()
        
    
    def getHeaderData(self):
        form = self.request.form
        header = form.get('fields',[])
        
        row_head = [_('User ID'),_('Name')]
        
        if 'employee' in header:
            row_head.append(_('Employee number'))
        if 'position' in header:
            row_head.append(_('Position'))
        if 'product' in header:
            row_head.append(_('Product'))
        if 'division' in header:
            row_head.append(_('Division'))
        if 'ingress' in header:
            row_head.append(_('Ingress'))
        if 'country' in header:
            row_head.append(_('Country'))
        if 'state' in header:
            row_head.append(_('State'))
        if 'city' in header:
            row_head.append(_('City'))
        if 'place' in header:
            row_head.append(_('Place'))
        if 'region' in header:
            row_head.append(_('Region'))
        if 'distric' in header:
            row_head.append(_('District'))
            
        config = form.get('reporttype','')
        if config == 'average':
            row_head.extend([_('Average'),_('Opportunities')])
        else:
            row_head.extend([_('Score'),_('Start'),_('End'),_('Time')])
        return row_head
    
    def getBodyData(self):
        form = self.request.form
        header = form.get('fields',[])
        config = form.get('reporttype','')
        if config == 'all':
            data = self.context.getAllDataUsers()
        else:
            data = self.context.getGroupDataUsers()
        result = []
        for row in data:
            tmprow = []
            
            tmprow.append(row['userid'])
            name = row['member'].getFullname()
            tmprow.append(name)
        
            if 'employee' in header:
                tmprow.append(row['member'].getEmployee())
            if 'position' in header:
                tmprow.append(row['member'].getPositionName())
            if 'product' in header:
                tmprow.append(','.join(row['member'].getProductName()))
            if 'division' in header:
                tmprow.append(','.join(row['member'].getDivisionName()))
            if 'ingress' in header:
                tmprow.append(str(row['member'].getIngress()))
            if 'country' in header:
                tmprow.append(row['member'].getCountryName())
            if 'state' in header:
                tmprow.append(row['member'].getState())
            if 'city' in header:
                tmprow.append(row['member'].getCity())
            if 'place' in header:
                tmprow.append(row['member'].getPlace())
            if 'region' in header:
                tmprow.append(row['member'].getRegion())
            if 'distric' in header:
                tmprow.append(row['member'].getDistrict())
        
            if config == 'average':
                tmprow.append(str(row['average']))
                tmprow.append(str(row['oportunities']))
            else:   
                tmprow.append(str(row['score']))
                tmprow.append(row['start'])
                tmprow.append(row['end'])
                tmprow.append(row['time'])
                
            result.append(tmprow)
            
        return result
        
    def setXLSHeaders(self, filename):    
        response = self.request.response
        response.setHeader('Content-Disposition', 'attachment; filename=' + filename)
        response.setHeader('Content-Type', 'application/vnd.ms-excel; charset=utf-8')
        #response.setHeader("Content-type: application/x-msexcel")
    
    def export_csv(self):
        filename = self.context.getId()+'-report.dat'
        self.setXLSHeaders(filename)
        output = '\t'.join(self.getHeaderData()) + '\n'
        for x in self.getBodyData():
            output += '\t'.join(x) + '\n'
        
        return u'%s' % output
    
    def export_xls(self):
        filename = self.context.getId()+'-report.xls'
        self.setXLSHeaders(filename)
        xml = ViewPageTemplateFile('templates/excel_xml.pt')
        #return u'%s' % xml()
        return xml()
    