# -*- coding: utf-8 -*-
"""
Defines all specific fields used on a quiz
"""

# Python imports
from types import StringType, UnicodeType, ListType, TupleType, BooleanType

# Zope imports
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

# Archetypes imports
from Products.Archetypes.public import *
from Products.Archetypes.Field import ObjectField, decode, encode
from Products.Archetypes.Registry import registerField

# Products imports
from widget import AnswerWidget

class AnswerField(ObjectField):
    """Field to store answers of a quiz"""
    
    __implements__ = ObjectField.__implements__
    _properties = Field._properties.copy()
    _properties.update({
        'type' : 'answer',
        'default' : (),
        'widget' : AnswerWidget,
        })

    security  = ClassSecurityInfo()

    security.declarePrivate('set')
    def set(self, instance, value, **kwargs):
        # Value is a list of tuple (<Answer:string>, <Checked:boolean>)
        if type(value) not in (ListType, TupleType):
            raise ValueError, "Value must be a list"

        for item in value:
            if not item or \
               type(item) not in (ListType, TupleType) or \
               len(item) != 2 or \
               type(item[0]) not in (StringType, UnicodeType) or \
               type(item[1]) not in (BooleanType,):
                raise ValueError, "list must contain tuple (<Answer:string>, <Checked:boolean>)"
        
        # Decode answer which is a string
        decoded_value = tuple([(decode(x[0].strip(), instance, **kwargs), x[1]) 
                            for x in value])
        
        ObjectField.set(self, instance, decoded_value, **kwargs)

    security.declarePrivate('get')
    def get(self, instance, **kwargs):
        value = ObjectField.get(self, instance, **kwargs) or {}
        encoded_value = tuple([(encode(x[0], instance, **kwargs), x[1])
                for x in value])
        return encoded_value

    security.declarePrivate('getRaw')
    def getRaw(self, instance, **kwargs):
        return self.get(instance, **kwargs)

    security.declarePublic('get_size')
    def get_size(self, instance, **kwargs):
        """Get size of the stored data used for get_size in BaseObject
        """
        
        return len(self.get(instance, **kwargs))

InitializeClass(AnswerField)

registerField(
    AnswerField,
    title='Answer',
    description='Used to store answer of a question.',
    )
