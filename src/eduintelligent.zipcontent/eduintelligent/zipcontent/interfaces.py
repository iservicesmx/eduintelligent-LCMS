from zope.interface import Interface
from zope import schema

from eduintelligent.zipcontent import zipcontentMessageFactory as _
from eduintelligent.zipcontent.formlib.interfaces import INamedFile

class IZipContent(Interface):
    """A folder containing courses
    """
    title = schema.TextLine(title=_(u"Title"),
                            required=True)
    
    description = schema.SourceText(title=_(u"Description"),
                                  description=_(u"A short summary of this folder"))
    
    filename = schema.Object(schema=INamedFile,
                             title=_(u"Zip File"),
                             description=_(u"The path of the zip package on your local machine."),
                             required=False)
    
    #track = schema.List(title=_(u"Track"))
