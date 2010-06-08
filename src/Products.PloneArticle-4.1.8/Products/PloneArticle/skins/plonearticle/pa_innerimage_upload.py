## Script (Python) "pa_innerimage_upload"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=field_name=None, new_file_title='', new_file_description='', new_file=None, widget_index=None
##title=Upload image
##

return context.pa_innercontent_upload(
    field_name=field_name,
    widget_index=widget_index, 
    max_size_property="imageMaxSize", 
    max_size_field_name="attachedImage",
    title=new_file_title, 
    description=new_file_description, 
    attachedImage=new_file)
