## Script (Python) "pa_thumb"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Returns a cacheable thumbnail
##

from Products.CMFCore.utils import getToolByName
NotFound = "NotFound"
request = context.REQUEST
response = request.RESPONSE

if len(traverse_subpath) < 1:
    raise NotFound, "Unknown page."

thumbnail_id = traverse_subpath[0]
abtool = getToolByName(context, 'plonearticle_tool')

try:
    return abtool.getThumbnail(context, thumbnail_id, request)
except:
    raise NotFound, "Unknown page."