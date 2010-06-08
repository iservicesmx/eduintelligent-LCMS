## Script (Python) "pa_manage_images_options"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=imageMaxSizes, referenceableImageTypes
##title=
##
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
tool = getToolByName(context, 'plonearticle_tool')

## the dict on which we loop must contain all the portal types
for portal_type, imageMaxSize in imageMaxSizes.items():
    referenceableImageType = referenceableImageTypes.get(portal_type, [])
    ## if portal_type in previewsAllowed.keys() then previewAllowed = True else...
    tool.setOptionsForType(portal_type, "image", "referenceableImageType",
                           referenceableImageType = referenceableImageType,
                           imageMaxSize = imageMaxSize,
                           )

message = _(u'Changes saved.')
context.plone_utils.addPortalMessage(message)
return state
