"""Definition of the QuestionXXXXX content type.
"""

from zope.interface import implements
from zope.component import adapts

from Acquisition import aq_inner

from Products.Archetypes import atapi
from Products.validation import V_REQUIRED

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.CMFCore.utils import getToolByName

from eduintelligent.evaluation.utility import hideMetadataSchema
from eduintelligent.evaluation.interfaces import IQuestionFillIn, IQuestion
from eduintelligent.evaluation.config import PROJECTNAME
from eduintelligent.evaluation import evaluationMessageFactory as _
from eduintelligent.evaluation.content.schemas import questionchoice_schema, base_question_schema
from eduintelligent.evaluation.content.question import Question

QuestionFillInSchema = schemata.ATContentTypeSchema.copy() + base_question_schema.copy()

QuestionFillInSchema['title'].widget = atapi.TextAreaWidget()
QuestionFillInSchema['title'].storage = atapi.AnnotationStorage()
QuestionFillInSchema['title'].widget.label = _(u"Question")
QuestionFillInSchema['title'].widget.description = _(u"")

finalizeATCTSchema(QuestionFillInSchema, folderish=False, moveDiscussion=False)
hideMetadataSchema(QuestionFillInSchema, excludeFromNav=True)

QuestionFillInSchema['description'].widget.visible = False

class QuestionFillIn(Question):
    """Describe a film.
    """
    implements(IQuestion, IQuestionFillIn)
    
    portal_type = "QuestionFillIn"
    _at_rename_after_creation = True
    schema = QuestionFillInSchema
    
    title = atapi.ATFieldProperty('title')
    
    def getTypeQuestion(self):
        return 'fill-in'

    
atapi.registerType(QuestionFillIn, PROJECTNAME)

