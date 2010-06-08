## Script (Python) "exportUsers"
## parameters=format='tab'
## title=
##
REQUEST  = context.REQUEST
RESPONSE = REQUEST.RESPONSE

export = context.portal_tctool
utool = context.portal_url
my_url =utool.getRelativeContentURL(context)

return export.exportCsvUser(url=my_url)
