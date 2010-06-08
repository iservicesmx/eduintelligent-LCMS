from zope.interface import Interface
from zope import schema
from zope.viewlet.interfaces import IViewletManager

from eduintelligent.evaluation import evaluationMessageFactory as _



class IBannerProvider(Interface):
    """A component which can provide an HTML tag for a banner image
    """    
    tag = schema.TextLine(title=_(u"A HTML tag for a banner image"))

class IEvaluation(Interface):
    """A folder containing evaluations
    """
    title = schema.TextLine(title=_(u"Title"),
                            required=True)
    description = schema.TextLine(title=_(u"Description"),
                            description=_(u"A short summary of this folder"))


class IExam(IEvaluation):
    """A folder containing exams
    """
    title = schema.TextLine(title=_(u"Title"),
                            required=True)
    description = schema.TextLine(title=_(u"Description"),
                                  description=_(u"A short summary of this folder"))

class IQuiz(IEvaluation):
    """A folder containing quizzes
    """
    title = schema.TextLine(title=_(u"Title"),
                          required=True)
    description = schema.TextLine(title=_(u"Description"),
                                description=_(u"A short summary of this folder"))

class IQuestionLetManager(IViewletManager):
    """ A Viewlet manager that renders a set of tabs for RealEstateContent
    objects."""


class IQuestion(Interface):
    """A Question
    """
    title = schema.TextLine(title=_(u"Question"),
                            required=True)

class IGroupQuestion(IQuestion):
    """A folder containing groupquestions
    """
    title = schema.TextLine(title=_(u"Title"),
                            required=True)
    description = schema.TextLine(title=_(u"Description"),
                                  description=_(u"A short summary of this folder"))

class IQuestionChoice(IQuestion):
    """A Question
    """
    title = schema.TextLine(title=_(u"Question"),
                            required=True)

class IQuestionFillIn(IQuestion):
    """A Question
    """
    title = schema.TextLine(title=_(u"Question"),
                            required=True)

