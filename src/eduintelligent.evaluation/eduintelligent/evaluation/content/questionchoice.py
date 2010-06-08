"""Definition of the QuestionXXXXX content type.
"""
import random

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
from eduintelligent.evaluation.interfaces import IQuestion, IQuestionChoice
from eduintelligent.evaluation.config import PROJECTNAME
from eduintelligent.evaluation import evaluationMessageFactory as _
from eduintelligent.evaluation.content.schemas import questionchoice_schema, base_question_schema
from eduintelligent.evaluation.content.question import Question

QuestionChoiceSchema = schemata.ATContentTypeSchema.copy() + questionchoice_schema.copy() + base_question_schema.copy()

QuestionChoiceSchema['title'].widget = atapi.TextAreaWidget()
QuestionChoiceSchema['title'].storage = atapi.AnnotationStorage()
QuestionChoiceSchema['title'].widget.label = _(u"Question")
QuestionChoiceSchema['title'].widget.description = _(u"")

finalizeATCTSchema(QuestionChoiceSchema, folderish=False, moveDiscussion=False)
hideMetadataSchema(QuestionChoiceSchema, excludeFromNav=True)

QuestionChoiceSchema['description'].widget.visible = False

class QuestionChoice(Question):
    """Describe a film.
    """
    implements(IQuestion, IQuestionChoice)
    
    portal_type = "QuestionChoice"
    _at_rename_after_creation = False
    schema = QuestionChoiceSchema
    
    title = atapi.ATFieldProperty('title')

    def post_validate(self, REQUEST=None, errors=None):
        """Extra validation
        """
        
        # Check answers
        answers = REQUEST.form.get('answers', None)
        error = False
        if answers is None:
            error = True
        elif len(answers) < 2:
            error = True
        elif len([x for x in answers if x.get('checked', False)]) < 1:
            error = True
            
        if error:
            errors['answers'] = _('you must select a least one correct answer')
        return

    
    def getTypeQuestion(self):
        return 'choice'
        
    def getAnswersOrdered(self):
        answers = [(x,y[0]) for x,y in enumerate(self.getAnswers())]
        if self.viewAnswersRandomOrder():
            answers.sort(lambda x,y: cmp(random.randint(0,200),100))
        return answers
        
    def getCorrectAnswerIds(self):
        """Returns ids of correct answers
        First question had id 0. Next has id 1 and go on.
        """
        answers = self.getAnswers()
        return [x for x in range(0, len(answers)) if answers[x][1]]


    def getCorrectAnswersCount(self):
        """Returns the number of correct answers defined"""

        return len(self.getCorrectAnswerIds())

    def getAnswerTitles(self, answer_ids):
        """Returns answer titles

        @param answer_ids: Ids of answers you want to get Title
        """

        answers = self.getAnswers()
        return [answers[x][0] for x in range(0, len(answers)) if x in answer_ids]
        
    def getCorrectAnswerTitles(self):
        answers = self.getCorrectAnswerIds()
        return self.getAnswerTitles(answers)
    
    def getTypeInput(self):
        return len(self.getCorrectAnswerIds()) > 1 and 'checkbox' or 'radio'
        
    def getResult(self, answers):
        correct_answer_ids =  self.getCorrectAnswerIds()
        return len([x for x in correct_answer_ids if x in answers]) == len(correct_answer_ids)


atapi.registerType(QuestionChoice, PROJECTNAME)

