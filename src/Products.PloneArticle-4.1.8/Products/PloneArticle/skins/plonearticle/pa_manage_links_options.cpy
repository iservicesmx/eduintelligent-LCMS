## Script (Python) "pa_manage_links_options"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=referenceableLinkTypes={}
##title=
##
# $Id: pa_manage_links_options.cpy 6193 2007-07-25 15:49:37Z glenfant $
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
tool = getToolByName(context, 'plonearticle_tool')

for portal_type, referenceableLinkType in referenceableLinkTypes.items():
    tool.setOptionsForType(portal_type, "links", "referenceableLinkType",
                           referenceableLinkType = referenceableLinkType
                           )
message = _(u'Changes saved.')
context.plone_utils.addPortalMessage(message)
return state

