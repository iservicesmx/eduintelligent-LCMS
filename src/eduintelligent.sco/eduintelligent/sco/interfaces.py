from zope.interface import Interface
from zope import schema

#from zope.app.container.constraints import contains
#from zope.app.container.constraints import container

from eduintelligent.sco import scoMessageFactory as _
from eduintelligent.sco.formlib.interfaces import INamedFile


class ISCO(Interface):
    """A folder containing courses
    """
    title = schema.TextLine(title=_(u"Title"),
                            required=True)
                            
    description = schema.SourceText(title=_(u"Description"),
                                  description=_(u"A short summary of this folder"))
                                  
    filename = schema.Object(schema=INamedFile,
                             title=u"SCORM File",
                             description=u"The name of the scrom package on your local machine.",
                             required=False)
                                  
    #track = schema.List(title=_(u"Track"))
    #track = schema.List()