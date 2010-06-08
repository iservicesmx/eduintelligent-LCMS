from zope.interface import Attribute
from zope.app.file.interfaces import IFile

class INamedFile(IFile):
    filename = Attribute("Filename")

