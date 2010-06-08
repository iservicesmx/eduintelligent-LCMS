from zope.interface import implements
from zope.app.file.file import File
from zope.app.form.browser.textwidgets import FileWidget
from eduintelligent.sco.formlib.interfaces import INamedFile

class NamedFile(File):
    implements(INamedFile)

    def __init__(self, data='', contentType='', filename=None):
        File.__init__(self, data, contentType)
        self.filename=filename


class NamedFileWidget(FileWidget):
    """A correctly working File widget.

    The standard FileWidget returns a string instead of an IFile instance,
    which means it will always fail schema validation in formlib.

    In addition this widget will also extract the filename and Content-Type
    from the request.
    """

    def _toFieldValue(self, input):
        value=super(NamedFileWidget, self)._toFieldValue(input)
        if value is not self.context.missing_value:
            filename=getattr(input, "filename", None)
            contenttype=input.headers.get("content-type",
                                          "application/octet-stream")
            value=NamedFile(value, contenttype, filename)

        return value

