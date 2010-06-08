## Script (Python) "pa_innerlink_upload"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=field_name,  new_url, new_title='', new_description='', widget_index=None
##title=
##

return context.pa_innercontent_upload(
    field_name=field_name,
    widget_index=widget_index, 
    max_size_property=None, 
    max_size_field_name=None,
    title=new_title, 
    description=new_description, 
    attachedLink=new_url)