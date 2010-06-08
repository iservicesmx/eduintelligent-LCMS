"""Define a browser view for the CourseFolder content type. In the FTI 
configured in profiles/default/types/*.xml, this is being set as the default
view of that content type.
"""

from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from eduintelligent.courses.interfaces import ICourse

from plone.memoize.instance import memoize

class CourseFolderView(BrowserView):
    """Default view of a courses folder
    """
    
    # This template will be used to render the view. An implicit variable
    # 'view' will be available in this template, referring to an instance
    # of this class. The variable 'context' will refer to the cinema folder
    # being rendered.
    
    __call__ = ViewPageTemplateFile('templates/coursefolder.pt')
    
    # Methods called from the associated template
    
    def have_categories(self):
        return len(self.categories()) > 0
    
    # The memoize decorator means that the function will be executed only
    # once (for a given set of arguments, but in this case there are no
    # arguments). On subsequent calls, the return value is looked up from a
    # cache, meaning we can call this function several times without a 
    # performance hit.
    
    @memoize
    def courses(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        
        # Note that we are cheating a bit here - to avoid having to "wake up"
        # the cinema object, we rely on our implementation that uses the 
        # Dublin Core Title and Description fields as title and address,
        # respectively. To rely only on the interface and not the 
        # implementation, we'd need to call getObject() and then use the
        # associated attributes of the interface, or we could add new catalog
        # metadata for these fields (with a catalog.xml GenericSetup file).

        return [ dict(url=course.getURL(),
                      title=course.Title,
                      description=course.Description,
                      category=course.category)
                 for course in 
                    catalog(object_provides=ICourse.__identifier__,
                            path=dict(query='/'.join(context.getPhysicalPath()),
                                      depth=1),
                            sort_on='sortable_title')
               ]
    @memoize
    def categories(self):
        """
        """
        context = aq_inner(self.context)
        categories = context.getCategories()
        return [dict(category=cat,content=self.courses(cat)) for cat in categories]
        