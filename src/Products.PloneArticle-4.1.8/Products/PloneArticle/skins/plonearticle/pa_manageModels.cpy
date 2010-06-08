## Script (Python) "pa_manageModels"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=default_views, models
##title=
##
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
tool = getToolByName(context, 'plonearticle_tool')

for portal_type, templates in models.items():
    default_view = default_views[portal_type]
    tool.setEnabledModelsForType(portal_type, templates, default_view)

message = _(u'Changes saved.')
context.plone_utils.addPortalMessage(message)
return state
