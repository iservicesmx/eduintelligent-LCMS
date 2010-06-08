## Script (Python) "pa_innerfile_upload"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=field_name, new_file_title='', new_file_description='', new_file=None, widget_index=None
##title=
##

return context.pa_innercontent_upload(
    field_name=field_name,
    widget_index=widget_index, 
    max_size_property="attachmentMaxSize", 
    max_size_field_name="attachedFile",
    title=new_file_title, 
    description=new_file_description, 
    attachedFile=new_file)
