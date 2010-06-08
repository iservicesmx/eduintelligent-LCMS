"""Define a browser view for the SCO content type. In the FTI 
configured in profiles/default/types/*.xml, this is being set as the default
view of that content type.
"""

from zope.component import createObject
from zope.formlib import form
from zope.app.form.browser.textwidgets import FileWidget
from Acquisition import aq_inner
from plone.app.form import base

from eduintelligent.sco import scoMessageFactory as _
from eduintelligent.sco.interfaces import ISCO
from eduintelligent.sco.formlib.interfaces import INamedFile
from eduintelligent.sco.formlib.file import NamedFileWidget

sco_form_fields = form.Fields(ISCO)
sco_form_fields['filename'].custom_widget = NamedFileWidget

class SCOAddForm(base.AddForm):
    """Add form for projects
    """    
    form_fields = sco_form_fields
    
    label = _(u"Add SCO")
    form_name = _(u"Add SCO")
            
    def create(self, data):
        sco = createObject(u"eduintelligent.sco.SCO")
        form.applyChanges(sco, self.form_fields, data)
        return sco

    
class SCOEditForm(base.EditForm):
    """Edit form for projects
    """
    form_fields = sco_form_fields
    
    label = _(u"Edit Project")
    form_name = _(u"Project settings")
    