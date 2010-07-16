## Script (Python) "exportUsersByGroup"
## parameters=format='tab'
## title=
##
REQUEST  = context.REQUEST
RESPONSE = REQUEST.RESPONSE
try:
    bygroup = REQUEST['groupname']
except KeyError:
    return
export = context.portal_tctool
utool = context.portal_url
my_url =utool.getRelativeContentURL(context)

return export.exportCsvUserByGroup(group=bygroup, url=my_url)
