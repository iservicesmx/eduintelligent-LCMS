# -*- coding: utf-8 -*-
"""
Defines all specific widgets used on a quiz
"""

# Python imports
from types import DictType

# Zope imports
from AccessControl import ClassSecurityInfo

# Archetypes imports
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerWidget

class AnswerWidget(TypesWidget):
    __implements__ = TypesWidget.__implements__
    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro' : "answer_widget",
        'helper_js': ('answer_widget.js',), 
        })
    security = ClassSecurityInfo()
    
    security.declarePublic('process_form')
    def process_form(self, instance, field, form, empty_marker=(),
                     emptyReturnsMarker=False):
        """ ... """
        
        value = form.get(field.getName(), empty_marker)
        if value is empty_marker: return empty_marker
        # Value is a list of tuple not a list of dictionary
        new_value = []
        for item in value:
            if not item:
                continue
            answer = item['answer']
            if not answer:
                continue
            
            checked = item.get('checked', False)
            new_value.append((answer, checked,))
        new_value = tuple(new_value)
        return new_value, {}

registerWidget(
    AnswerWidget,
    title='Answer grid',
    description=('A data grid, to enter all possible answers'),
    used_for=('eduintelligent.evaluation.content.field.AnswerField',)
    )