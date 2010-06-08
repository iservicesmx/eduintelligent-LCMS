""" Faq Folder Class """

from interfaces import IFaqFolder
from zope.interface import implements
from Products.Archetypes.public import *

try:
    # If LinguaPlone exists, use it:
    from Products.LinguaPlone.I18NOrderedBaseFolder import I18NOrderedBaseFolder as OrderedBaseFolder
except ImportError:
    # Use the one in Archetypes (already imported)
    pass
    
schema = BaseFolderSchema + Schema((
    TextField('description',
              widget=TextAreaWidget(description_msgid="desc_folder",
                                    description="The description of the FAQ category.",
                                    label_msgid="label_folder",
                                    label="Description",
                                    i18n_domain = "faq",
                                    rows=6)),
    IntegerField('delay',
                 widget=IntegerWidget(description="Delay for a new item.",
                                      description_msgid="desc_delay",
                                      label_msgid="label_delay",
                                      label="Delay",
                                      i18n_domain = "faq"),
                 default=7,
                 required=1,
                 searchable=0,
                 validators=('isInt',)),
    ))

class FaqFolder(OrderedBaseFolder):
    """A simple folderish archetype Folder"""

    implements(IFaqFolder)
    
    schema = schema
    _at_rename_after_creation = True

registerType(FaqFolder)
