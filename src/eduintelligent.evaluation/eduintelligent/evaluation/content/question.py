"""Definition of the Question content type.
"""

from zope.interface import implements
from zope.component import adapts

from Acquisition import aq_inner

from Products.Archetypes import atapi

from Products.ATContentTypes.content import base

from Products.CMFCore.utils import getToolByName

from eduintelligent.evaluation.interfaces import IQuestion
from eduintelligent.evaluation.interfaces import IBannerProvider


class Question(base.ATCTContent):
    """Describe a question
    """
    implements(IQuestion)
    portal_type = "Question"
    _at_rename_after_creation = False

    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        return self.getField('qimage').tag(self, **kwargs)

    def __bobo_traverse__(self, REQUEST, name):
        """Give transparent access to image scales. This hooks into the
        low-level traversal machinery, checking to see if we are trying to
        traverse to /path/to/object/image_<scalename>, and if so, returns
        the appropriate image content.
        """
        if name.startswith('qimage'):
            field = self.getField('qimage')
            image = None
            if name == 'qimage':
                image = field.getScale(self)
            else:
                scalename = name[len('qimage_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image

        return super(Question, self).__bobo_traverse__(REQUEST, name)


# This simple adapter uses Archetypes' ImageField to extract an HTML tag
# for the banner image. This is used in the promotions portlet to avoid
# having a hard dependency on the AT ImageField implementation.

# Note that we adapt a class, not an interface. This means that we will only
# match adapter lookups for this class (or a subclass), which is correct in
# this case, because we are relying on internal implementation details.

class BannerProvider(object):
    implements(IBannerProvider)
    adapts(Question)

    def __init__(self, context):
        self.context = context

    @property
    def tag(self):
        return self.context.getField('qimage').tag(self.context, scale='thumb')
