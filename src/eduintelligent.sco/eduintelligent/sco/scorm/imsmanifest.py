#
# imsmanifest.py - accessing the XML structure of an IMS manifest file
#
# Copyright (C) 2005 Ralph Barthel - ralph.barthel@21ll.com
#                    Helmut Merz - helmutm@cy55.de
#
# Copyright (C) 2007 Erik Rivera Morales - erik@ro75.com
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the
#    Free Software Foundation, Inc., 59 Temple Place, Suite 330,
#    Boston, MA  02111-1307  USA
"""

$Id: imsmanifest.py 510 2005-07-19 07:14:45Z rbarthel $
"""

from xml.dom import minidom
#import utils

#class IMSManifest(object):  # maybe we better stay compatible to Zope 2.7 still:
class IMSManifest:
    """ A convenience interface to a DOM structure built from an
        IMS manifest XML file.
    """

    __allow_access_to_unprotected_subobjects__ = 1

    def __init__(self, src):
        self.document = minidom.parseString(src)
        
    def getStartResource(self, scorm_id=None):
        resources = self.document.getElementsByTagName('resources')
        # Should better check for scormtype == 'sco':
        startResource = None
        if scorm_id is None:
            startResource = resources[0].getElementsByTagName('resource')[0]
        else:
            listResources = resources[0].getElementsByTagName('resource')
            for r in listResources:
                if r.getAttribute('identifier')== scorm_id:
                    startResource = r
                    break
        addParam=""
        items = self.document.getElementsByTagName('item')
        for i in items:
             if i.getAttribute('identifierref')== scorm_id and i.getAttribute('parameters'):
                    addParam = i.getAttribute('parameters')
                    break
        if startResource:
            if addParam!="":
                return startResource.getAttribute('href')+"?"+addParam
            else:
                return startResource.getAttribute('href')
        else:
            raise ValueError, "No Resource with identifier %s" % scorm_id
            
    def getItems(self, parent=None):
        listItems=[]
        children= parent.childNodes
        for c in children:
            if c.nodeName == "item":
                listItems.append(c)
        
        return listItems

    def getItemCount(self):
        return len(self._getItems())

    def getItemTitle(self, item=0):
        return self._getItemData('title', item)

    def getIdentifier(self, nodeElem):
        return nodeElem.getAttribute('identifier')
	
    def getIdentifierRef(self, itemId):
        return self.getItemIdentifier(itemId)

    def getSubItems(self, orgElem):
        return self._getOrgChildren(orgElem)

    def getItem(self, itemId):
        items = self._getItems()
        msg = 'Item not found'
        for item in items:
            if (item.getAttribute('identifier')) == itemId:
                return item
        return msg
        
    def hasItemNodes(self, itemId):
        items = self._getItems()
        chkNode = None
        for item in items:
            if (item.getAttribute('identifier')) == itemId:
                chkNode = item
                break
        listNodes = self.getItems(chkNode)
        return listNodes
        
    def getLevel(self, pNode, cNode):
        counter = 0
        while cNode.parentNode != pNode:
            cNode = cNode.parentNode
            counter += 1
        return counter    
        
    def getLaunchData(self, item=0):
        # for reasons of backward compliance
        if  type(item) == type(0):
           return self._getItemData('adlcp:datafromlms', item)
        else:
           scormItems = self.document.getElementsByTagName('item')
           retVal='Item not found'
           for s in scormItems:
                if (s.getAttribute('identifier')) == item:
                    return self._getNodeData(s, 'adlcp:datafromlms') 
           return retVal
    
    def getMasteryScore(self, item=0):
        if  type(item) == type(0):
            return self._getItemData('adlcp:masteryscore', item)
        else:
            scormItems = self.document.getElementsByTagName('item')
            retVal='Item not found'
            for s in scormItems:
                if (s.getAttribute('identifier')) == item:
                    return self._getNodeData(s, 'adlcp:masteryscore') 
            return retVal
            
    def getOrganizations(self, documentNode=None):
        documentNode = documentNode or self.document
        return documentNode.getElementsByTagName('organization')
        
    def getOrganizationsNodes(self, documentNode=0):
        return self.document.getElementsByTagName('organizations')
        
    def isSCO(self, itemNode):
        idRef = itemNode.getAttribute('identifierref')
        resources = self.document.getElementsByTagName('resource')
        isSCO = True
        if idRef is not None and idRef != "":
            for r in resources:
                if (r.getAttribute('identifier')) == idRef:
                    if r.getAttribute('adlcp:scormtype') == "sco":
                        isSCO = False
                        break
        return isSCO
        
    def getTitle(self, nodeElem):
        return nodeElem.getElementsByTagName('title')[0].firstChild.nodeValue
    
    #this function enables backward compatibility to copy existing records based on numeric index.
    # it is sufficient to check the first hierarchie level as further hierarchy levels haven't been supported
    # up to that stage. Tests only for first organization elemnt as used in the projects context
    def getItemIndex(self, itemId):
        legacyItems = self._getItems()
        isIndexed= 0
        counter = 0
        for i in legacyItems:
            if (i.getAttribute('identifier')) == itemId:
                # record exist
                isIndexed = 1
                break
            counter = counter +1;   
        
        if isIndexed:
            return counter
        else:
            return -1
    
    def getItemIdentifier(self, itemId):
        items = self._getItems()
        for i in items:
            if (i.getAttribute('identifier')) == itemId:
                # record exist
                return i.getAttribute('identifierref')

    def domToList(self, orgElem):
        listOrg = []

    # private methods:

    def _getResourceURI(self, scorm_id):
        return ''

    def _getOrgChildren(self,orgElem):
        return orgElem.getElementsByTagName('item')
    
    def _getItems(self):
        organizations = self.document.getElementsByTagName('organizations')[0]
        orgs = organizations.getElementsByTagName('organization')
        if not orgs:
            return []
        firstOrg = orgs[0]
        # not ok, can heave more than one organization
        return firstOrg.getElementsByTagName('item')

    def _getFirstItem(self):
        items = self._getItems()
        return items and items[0] or None

    def _getItemData(self, tagname, index):
        items = self._getItems()
        if len(items) > index:
            tags = items[index].getElementsByTagName(tagname)
            if tags:
                return tags[0].childNodes[0].data
            else:
                return ''
        else:
            return ''
            
    #returns the data of a xml node, inparams: parentnode and name of the childelement which holds the data - rb
    def _getNodeData(self, nodeElem, childElem):
         dataNode = nodeElem.getElementsByTagName(childElem)
         if dataNode:
             return dataNode[0].childNodes[0].data
         else:
             return 'not found'
            
