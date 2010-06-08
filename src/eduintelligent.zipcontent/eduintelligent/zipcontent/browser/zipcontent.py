"""Define a browser view for the SCO content type. In the FTI 
configured in profiles/default/types/*.xml, this is being set as the default
view of that content type.
"""

from zope.component import createObject
from zope.formlib import form
from zope.app.form.browser.textwidgets import FileWidget
from Acquisition import aq_inner
from plone.app.form import base

from eduintelligent.zipcontent import zipcontentMessageFactory as _
from eduintelligent.zipcontent.interfaces import IZipContent
from eduintelligent.zipcontent.formlib.interfaces import INamedFile
from eduintelligent.zipcontent.formlib.file import NamedFileWidget

sco_form_fields = form.Fields(IZipContent)
sco_form_fields['filename'].custom_widget = NamedFileWidget

class ZipContentAddForm(base.AddForm):
    """Add form for projects
    """    
    form_fields = sco_form_fields
    
    label = _(u"Add ZipContent")
    form_name = _(u"Add ZipContent")
            
    def create(self, data):
        sco = createObject(u"eduintelligent.zipcontent.ZipContent")
        form.applyChanges(sco, self.form_fields, data)
        return sco

    
class ZipContentEditForm(base.EditForm):
    """Edit form for projects
    """
    form_fields = sco_form_fields
    
    label = _(u"Edit ZipContent")
    form_name = _(u"Edit ZipContent")
    