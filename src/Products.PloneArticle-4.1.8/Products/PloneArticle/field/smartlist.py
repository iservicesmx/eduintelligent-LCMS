# -*- coding: utf-8 -*-
## Defines SmartListField
## 
## Copyright (C) 2006 Ingeniweb

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING. If not, write to the
## Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
Defines SmartListField
"""

__docformat__ = 'restructuredtext'

from types import DictType, ListType, TupleType

# Zope imports
from Acquisition import aq_base
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.PluginIndexes.interfaces import IUniqueValueIndex, IDateIndex, \
     IDateRangeIndex
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.Registry import registerField
from Products.Archetypes.Field import ReferenceField

from Products.ATContentTypes.criteria import _criterionRegistry
from Products.ATContentTypes.interface import IATTopicSearchCriterion
from Products.ATContentTypes.interface import IATTopicSortCriterion

#Products imports
from Products.PloneArticle.interfaces import ISmartListField
from Products.PloneArticle.widget import SmartListWidget

class SmartListField(ReferenceField):
    """
    A field that allow to reference content based on search criterias

    use 'allowed_types' to restrict selectable types
    """
    implements(ISmartListField)
    
    _properties = ReferenceField._properties.copy()
    _properties.update({
        'widget': SmartListWidget,
        'allowed_criterias': None, #catalog indexes allowed ids
        'default_criterias': (),
        'auto_reference': False,
        'results_len': 20, # number of results to show
        'sort_index': 'modified',
        'sort_order': 'reverse',
        })

    security  = ClassSecurityInfo()

    def __init__(self, name=None, **kwargs):
        """
        """
        ReferenceField.__init__(self, name, **kwargs)
        self.multiValued = True  # force multivalued
        self.search_criterias = {'SearchableText': '',
                                 'portal_types': (),
                                 }

    security.declarePublic('getAllowedTypes')
    def getAllowedTypes(self, instance):
        """Return the list of allowed portal_types for searching / referencing
        """
        pu = getToolByName(instance, 'plone_utils')
        allowed_types = list(self.allowed_types)
        return pu.getUserFriendlyTypes(allowed_types)


    security.declarePrivate('getAllowedCriterias')
    def getAllowedCriterias(self, instance):
        """return a tuple of allowed search criterias ids"""
        ct = getToolByName(instance, 'portal_catalog')
        criterias = self.allowed_criterias
        if criterias is None:
            criterias = ct.indexes()

        indexes = ct.getIndexObjects()
        criterias = [i.getId() for i in indexes
                     if i.getId() in criterias
                     and (i.getId() == 'SearchableText'
                          or (IUniqueValueIndex.providedBy(i)
                              and not (IDateIndex.providedBy(i) or
                                       IDateRangeIndex.providedBy(i))
                              )
                          )
                     ]
                     
        def lowcase_cmp(s1, s2):
            return cmp(s1.lower(), s2.lower())
        
        criterias.sort(lowcase_cmp)
        return tuple(criterias)

    security.declarePrivate('filterSearchCriterias')
    def filterSearchCriterias(self, instance, search_criterias):
        """
        Check params of search request, and remove invalids indexes
        """
        if type(search_criterias) is not DictType:
            raise TypeError, "Invalid type for search_criterias"

        allowed_criterias = self.getAllowedCriterias(instance)
        if allowed_criterias:
            for k in search_criterias.keys():
                if k not in allowed_criterias:
                    del search_criterias[k]

        # filter portal_type list
        # if portal_type is empty, fill it with searchable types
        pu = getToolByName(instance, 'plone_utils')
        searched_types = search_criterias.get('portal_type', [])
        searched_types = [t for t in searched_types if t != '']
        searched_types = pu.getUserFriendlyTypes(searched_types)

        #then intersect with field allowed_types
        allowed_types = self.getAllowedTypes(instance)
        search_criterias['portal_type'] = tuple([t for t in searched_types
                                                 if t in allowed_types])

        return search_criterias

    security.declarePublic('getAttrNameFor')
    def getAttrNameFor(self, propname):
        """
        Return the attribute name to look for on instance for storing property
        """
        return '%s_%s' % (self.getName(), propname)

    security.declarePublic('getSearchCriterias')
    def getSearchCriterias(self, instance):
        """
        Return a copy of current search_criterias dictionnary
        """
        search_criterias = getattr(instance.aq_explicit,
                                   self.getAttrNameFor('search_criterias'),
                                   self.search_criterias)
        return search_criterias.copy()

    security.declarePrivate('setSearchCriterias')
    def setSearchCriterias(self, instance, search_criterias):
        """
        adjust search_criterias dict to allowed queries and update field.
        This method has side-effect on 'search_criterias' variable.
        """
        search_criterias = self.filterSearchCriterias(instance, search_criterias)
        current = self.getSearchCriterias(instance)
        current.update(search_criterias)
        setattr(instance, self.getAttrNameFor('search_criterias'),
                self.filterSearchCriterias(instance, current))

    security.declarePublic('getExcludedUIDs')
    def getExcludedUIDs(self, instance):
        """
        Return the list of excluded uids
        """

        return getattr(aq_base(instance), self.getAttrNameFor('excluded_uids'),
                       {})

    security.declarePrivate('setExcludedUIDs')
    def setExcludedUIDs(self, instance, uids):
        """
        """
        if type(uids) is not DictType:
            raise TypeError, "expected a dictionnary, got %s" % repr(type(uids))
        
        setattr(instance, self.getAttrNameFor('excluded_uids'), uids)

    security.declarePublic('getAutoReference')
    def getAutoReference(self, instance):
        """
        """
        name = self.getAttrNameFor('auto_reference')
        return getattr(instance, name, self.auto_reference)

    security.declarePrivate('setAutoReference')
    def setAutoReference(self, instance, auto_ref):
        """
        """
        name = self.getAttrNameFor('auto_reference')
        setattr(instance, name, auto_ref)
        
    security.declarePublic('searchContents')
    def searchContents(self, instance, search_criterias=None):
        """
        return the 20 first brains sort on 'sort_index'
        """
        if search_criterias is None:
            search_criterias = self.getSearchCriterias(instance)
        else:
            if type(search_criterias) is not DictType:
                raise TypeError, "Invalid type for search_criterias: %s" % type(search_criterias)
            search_criterias = search_criterias.copy()

        search_criterias = self.filterSearchCriterias(instance, search_criterias)

        for k, v in search_criterias.items():
            if not v: #FIXME: break with bool search
                del search_criterias[k]

        search_criterias['sort_on'] = self.sort_index
        search_criterias['sort_order'] = self.sort_order
        search_criterias['sort_limit'] = self.results_len

        ct = getToolByName(instance, 'portal_catalog')
        return  ct.searchResults(**search_criterias)[:self.results_len]

    security.declarePrivate('get')
    def get(self, instance, aslist=False, **kwargs):
        """
        Return referenced objects + newer if auto_reference is set
        """
        result = ReferenceField.get(self, instance, aslist, **kwargs)

        if not self.getAutoReference(instance):
            return result

        uid_ct = getToolByName(instance, 'uid_catalog')
        x_uids = self.getExcludedUIDs(instance)
        # also exclude 'real' references to avoid doublons
        x_uids.update(dict.fromkeys([o.UID() for o in result]))
        
        # search with empty would return all catalog
        if len(x_uids):
            x_uids = uid_ct.searchResults(UID={'query': x_uids.keys(),})
            x_uids = {}.fromkeys([b.getPath() for b in x_uids], True)

        # brains path from uid catalog are relative to portal root
        urlTool = getToolByName(instance, 'portal_url')
        portal_path = '/'.join(urlTool.getPortalObject().getPhysicalPath())
        portal_path_len = len(portal_path) + 1 # trailling '/' counted

        auto_refs = self.searchContents(instance)
        auto_refs = [b.getObject() for b in auto_refs
                     if not x_uids.has_key(b.getPath()[portal_path_len:])]
        result.extend(auto_refs)
        return result
    
    security.declarePrivate('set')
    def set(self, instance, value, search_criterias=None,
            uids_found=None, ref_uids=(), auto_reference=None, **kwargs):
        """
        Mutator.

        value: list of uids, must be included in uids_found
        search_criterias': {...},
        uids_found': [...],  # list presented to the user
        'auto_reference': True or False
               }

        The from value and ref_uids the field builds a list of excluded uids and
        merge it with existing exclusion list. From this exclusion list, it
        removed already referenced uids (it means the user has unchecked them).

        Then it merge the old reference list with the new value, and from this
        new value it removes uids listed for exclusion (it means the user have
        checked them).

        To delete references, you must do a 'set' with empty value and the
        uids you wish to unref listed in 'uids_found'
        """

        if type(value) not in (ListType, TupleType):
            raise (TypeError,
                   "Invalid type for value: expected list or tuple, got '%s'"
                   % type(value))

        if search_criterias is not None:
            self.setSearchCriterias(instance, search_criterias)

        if auto_reference is not None:
            self.setAutoReference(instance, bool(auto_reference))

        old_value = dict.fromkeys(ReferenceField.getRaw(self, instance,))

        # update excluded_uids with uids listed but not checked for inclusion
        excluded_uids = self.getExcludedUIDs(instance)
        old_excluded_count = len(excluded_uids)
        update_excluded = False

        if uids_found is not None:
            new_excluded = dict.fromkeys([uid for uid in uids_found
                                          if uid not in value],
                                         True)
            update_excluded = len(new_excluded) != 0
            # remove old refs if they have been unchecked in widget
            for uid in new_excluded.iterkeys():
                if old_value.has_key(uid):
                    del old_value[uid]
            excluded_uids.update(new_excluded)
            
        # compute new value ensuring unique items in list
        value = dict.fromkeys(value)
        value.update(old_value)
        value = value.keys()

        # remove old excluded_uids if they have been checked in widget
        for k in excluded_uids.keys():
            if k in value:
                del excluded_uids[k]

        update_excluded = (update_excluded or
                           (len(excluded_uids) != old_excluded_count))

        # write excluded uids only if it has changed
        if update_excluded:
            self.setExcludedUIDs(instance, excluded_uids)
            
        ReferenceField.set(self, instance, value, **kwargs)
    
registerField(SmartListField,
              title="SmartListField",
              description=SmartListField.__doc__)
