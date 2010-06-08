## Script (Python) "pa_innercontent_upload"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=field_name, widget_index=None, max_size_property=None, max_size_field_name=None, **kwargs
##title=
##

from Products.CMFCore.utils import getToolByName

request = context.REQUEST
pa_tool = getToolByName(context, 'plonearticle_tool')
utils = getToolByName(context, 'plone_utils')
field = context.getField(field_name)
template = context.restrictedTraverse(path='pa_temporary_innerimage_widget')

# help utranslate to write with proper encoding
charset = utils.getSiteEncoding()
request.RESPONSE.setHeader('Content-Type', 'text/html; charset=%s' % charset)

# Get size and check against max allowed size
if max_size_property is not None:
    # Check max size property
    file_to_check = kwargs.get('max_size_field_name', None)
    
    if file_to_check is not None:
        file_to_check.seek(0, 2)
        size = file_to_check.tell()
        file_to_check.seek(0)
        max_size = context.getTypeInfo().getProperty(max_size_property, None)
    
        if max_size is not None and size > max_size:
            message = context.utranslate(
                u'max_file_size_exceeded_error',
                mapping={
                    "max_size": context.getObjSize(context, max_size),
                    },
                default=u"Error: maximum allowed file size is ${max_size}",
                domain="plonearticle")
            return template(from_upload=True, skip_widget=True, fail_reason=message)

# Upload new content
accessor = field.getAccessor(context)
existing_ids = [c.getId() for c in accessor()]
tmp_content = field.getTemporaryInnerContent(context)
mutator = field.getMutator(context)
try:
    value = {"id": tmp_content.getId(),}
    value.update(kwargs)
    mutator((value,), update=True)
except:
    exception = context.plone_utils.exceptionString()
    message = "Uploaded content error: %s" % exception
    return template(from_upload=True, skip_widget=True, fail_reason=message)


# FIXME: This use case cannot happen. Maybe delete it
# Check if content has been added to article
new_inner_contents = [c for c in accessor()
                     if c.getId() not in existing_ids]

if len(new_inner_contents)!=1:
    exception = "Uploaded content has not been added"
    message = "Uploaded content error: %s" % exception
    return template(from_upload=True, skip_widget=True, fail_reason=message)

inner_content = new_inner_contents[0]

# Render template
widget = field.widget
if widget_index is None:
    widget_index = widget.generateWidgetIndex()   
widget_index = int(widget_index)

return template(from_upload=True,
                inner_content=inner_content,
                field=field,
                field_name=field_name,
                widget=widget,
                widget_index=widget_index)