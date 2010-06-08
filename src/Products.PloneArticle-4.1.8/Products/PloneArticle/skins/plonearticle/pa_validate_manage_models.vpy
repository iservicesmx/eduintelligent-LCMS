## Script (Python) "pa_validate_manage_models"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=default_views, models
##title=Validates default_view for PloneArticle models

default_message = 'The default model must be in available models'
error_message = context.utranslate(msgid='error_default_model_invalid', mapping={},
                                   default=default_message,
                                   domain='plonearticle',)
                                   

for portal_type, templates in models.items():
    default_view = default_views[portal_type]

    if not default_view in templates:
        state.setError(portal_type, error_message)

if state.getErrors():
    return state.set(status='failure', portal_status_message='Please correct the indicated errors.')
else:
    return state
