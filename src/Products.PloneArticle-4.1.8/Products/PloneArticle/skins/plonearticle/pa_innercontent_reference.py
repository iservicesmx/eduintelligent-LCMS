## Script (Python) "pa_innercontent_reference"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=field_name, uid, widget_index=None
##title=
##
from Products.CMFCore.utils import getToolByName

request = context.REQUEST
pa_tool = getToolByName(context, 'plonearticle_tool')
reference_tool = getToolByName(context, 'reference_catalog')
obj = reference_tool.lookupObject(uid)

if not obj:
    return context.standard_error_message(error_type=404,
     error_message="The link you followed appears to be broken")

field = context.getField(field_name)
tmp_content = field.getTemporaryInnerContent(context)
accessor = field.getAccessor(context)
existing_ids = [c.getId() for c in accessor()]
mutator = field.getMutator(context)
template = context.restrictedTraverse(path='pa_temporary_innerimage_widget')

# help utranslate to write with proper encoding
utils = getToolByName(context, 'plone_utils')
charset = utils.getSiteEncoding()
request.RESPONSE.setHeader('Content-Type', 'text/html; charset=%s' % charset)

# Reference new content
try:
    mutator(({"id": tmp_content.getId(),
              "title": obj.title_or_id(),
              "description": obj.Description(),
              "referencedContent": uid},),
             update=True)
except:
    exception = context.plone_utils.exceptionString()
    message = "Referenced content error: %s" % exception
    return template(from_upload=False, skip_widget=True, fail_reason=message)


# FIXME: This use case cannot happen. Maybe delete it
# Check if content has been added to article
new_inner_contents = [c for c in accessor()
                     if c.getId() not in existing_ids]

if len(new_inner_contents)!=1:
    exception = "Inner content has not been added"
    message = "Referenced content error: %s" % exception
    return template(from_upload=False, skip_widget=True, fail_reason=message)

inner_content = new_inner_contents[0]

# Render template
widget = field.widget
if widget_index is None:
    widget_index = widget.generateWidgetIndex()   
widget_index = int(widget_index)

return template(from_upload=False,
                inner_content=inner_content,
                field=field,
                field_name=field_name,
                widget=widget,
                widget_index=widget_index)