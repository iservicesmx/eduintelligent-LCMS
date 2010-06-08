## Script (Python) "importUsers"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=adds users to training center

from Products.CMFCore.utils import getToolByName

RESPONSE = context.REQUEST.RESPONSE

tctool = getToolByName(context, 'portal_tctool')
filename = context.REQUEST.get('filename',None)
if not filename:
    return
    
tctool.importCsvUser(context, filename)

return RESPONSE.redirect(context.absolute_url()+'/@@users')