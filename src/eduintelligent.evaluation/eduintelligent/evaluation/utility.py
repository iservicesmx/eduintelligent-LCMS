"""
"""

def hideMetadataSchema(schema, excludeFromNav=True, isDoc=False):
    """
    """
    for field in schema.fields():
        if field.isMetadata:
            field.schemata = 'default'
            field.widget.visible = False
    
    schema['description'].widget.visible = True
    
    # Ownership
    if schema.has_key('creators'):
        schema.changeSchemataForField('creators', 'ownership')
        schema['creators'].widget.visible = True
    if schema.has_key('contributors'):
        schema.changeSchemataForField('contributors', 'ownership')
        schema['contributors'].widget.visible = True
    if schema.has_key('rights'):
        schema['rights'].widget.visible = True
        schema.changeSchemataForField('rights', 'ownership')

    schema['excludeFromNav'].default = excludeFromNav
    
    # if isDoc:
    #     schema['rights'].widget.visible = True
    #     schema.changeSchemataForField('rights', 'ownership')
        

    return schema