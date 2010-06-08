# -*- coding: utf-8 -*-
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """Robert Niederreiter <robertn@bluedynamics.com>"""
__docformat__ = 'plaintext'


import Globals
from AccessControl import ClassSecurityInfo
from Products.Archetypes.utils import OrderedDict


class AlphaBatch(object):
    """Object used to batch results alphabetically.
    """
    
    security = ClassSecurityInfo()
    
    JOKER = '*'

    vocab = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
             'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
             JOKER]
             
    threshold = 20
    
    
    def __init__(self, results, context, request):
        """Take the results and the request.
        """
        self.context = context
        self.results = results
        self.currentresults = []
        self.pagemap = OrderedDict()
        self.request = request
        self.showBatch = True
                
        if len(results) < self.threshold:
            self.showBatch = False
            self.currentresults = results
        else:
            self.initialize()
    
    def initialize(self):
        """Initialize this batch object.
        """
        current = self.request.get('currentPage', None)
        pointer = 0
        hasResults = len(self.results)
        nonresults = []
        
        for term in self.vocab:
            
            # full init for term
            self.pagemap[term] = dict()
            self.pagemap[term]['value'] = term
            self.pagemap[term]['visible'] = False
            self.pagemap[term]['current'] = False
            
            # special handling for joker
            if term == self.JOKER:
                continue
            
            # assume alpha sorted results here
            for result in self.results[pointer:]:                
                title = result['fullname'].upper()
                title.replace('ü','Ü')
                title.replace('ö','Ö')
                title.replace('ä','Ä')
                
                currentTerm = title and title[0] or None
                if currentTerm is None or currentTerm not in self.vocab:
                    nonresults.append(result)
                    pointer += 1
                    continue
                
                if title.startswith(term):
                    self.pagemap[term]['visible'] = True
                    if current is None:
                        current = term
                    if term == current:
                        self.currentresults.append(result)
                    pointer += 1
                else:
                    break
            
            # check for current after processing
            if term == current:
                self.pagemap[term]['current'] = True

        if nonresults:
            self.pagemap[self.JOKER]['visible'] = True
        if current == '*':
            self.currentresults = nonresults
            self.pagemap[self.JOKER]['current'] = True
            
    
    security.declarePublic('showBatch') 
    def showBatch(self):
        """Return True if results reaches threshold.
        """
        return self.showBatch
    
    security.declarePublic('getPages')    
    def getPages(self):
        """Return a list of dicts containing page definitions.
        """
        return self.pagemap.values()
    
    security.declarePublic('getResults')
    def getResults(self):
        """Return the current result.
        """
        return self.currentresults

Globals.InitializeClass(AlphaBatch) 