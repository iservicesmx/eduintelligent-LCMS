## Script (Python) "pa_create_inner_content_widget"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=field_name, widget_index=None
##title=Returns html code of a new inner content widget
##
##
field = context.getField(field_name)
widget = field.widget
inner_content = field.getTemporaryInnerContent(context)

if widget_index is None:
    widget_index = widget.generateWidgetIndex()
    
widget_index = int(widget_index)

# Render template
template = context.restrictedTraverse(path='pa_new_inner_content_widget')
return template(field_name=field_name, field=field, widget=widget,
                widget_index=widget_index, inner_content=inner_content)
