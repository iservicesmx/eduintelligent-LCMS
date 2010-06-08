## Script (Python) "getRelPath"
##title=Helper method for ploneArticle Browser
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=path


portal=context.portal_url.getPortalObject()
portalPath=portal.getPhysicalPath()  
bPath=path.split('/')
lenPPath = len(portalPath)
relPath = '/'.join(bPath[lenPPath:])

return relPath
