## Script (Python) "pa_manage_attachments_forms"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=referenceableAttachmentTypes, attachmentMaxSizes, previewsAllowed={}
##title=
##
# $Id: pa_manage_attachments_options.cpy 6193 2007-07-25 15:49:37Z glenfant $
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

tool = getToolByName(context, 'plonearticle_tool')

## the dict on which we loop must contain all the portal types
for portal_type, attachmentMaxSize in attachmentMaxSizes.items():
    referenceableAttachmentType = referenceableAttachmentTypes.get(portal_type, [])
    ## if portal_type in previewsAllowed.keys() then previewAllowed = True else...
    previewAllowed = portal_type in previewsAllowed.keys()
    tool.setOptionsForType(
        portal_type, "attachment", "referenceableAttachmentType",
        referenceableAttachmentType = referenceableAttachmentType,
        attachmentMaxSize = attachmentMaxSize,
        previewAllowed = previewAllowed,
        )

message = _(u'Changes saved.')
context.plone_utils.addPortalMessage(message)
return state

