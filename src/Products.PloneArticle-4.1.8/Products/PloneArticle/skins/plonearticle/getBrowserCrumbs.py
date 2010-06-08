## Script (Python) "getBrowserCrumbs"
##title=Helper method for getting browser crumbs
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=obj=None

if not obj : 
   obj=context

from Products.CMFCore.utils import getToolByName

ct = getToolByName(context, 'portal_catalog')
stp = getToolByName(context, 'portal_properties').site_properties
query = {}


currentPath = '/'.join(obj.getPhysicalPath())
query['path'] = {'query':currentPath, 'navtree':1, 'depth': 0}

rawresult = ct(**query)

# Sort items on path length
dec_result = [(len(r.getPath()),r) for r in rawresult]
dec_result.sort(lambda x, y: cmp(x[0], y[0]))

result = []
for r_tuple in dec_result:
    item = r_tuple[1]
    item_path = item.getPath()
    data = {'Title': item.pretty_title_or_id(),
            'path': item_path}
    result.append(data)
return result
