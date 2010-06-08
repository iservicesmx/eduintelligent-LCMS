"""Definition of the Exam content type.
"""

import random

from zope.interface import implements
from Products.Archetypes import atapi

from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.CMFCore.utils import getToolByName

from eduintelligent.evaluation.utility import hideMetadataSchema
from eduintelligent.evaluation.interfaces import IQuiz, IEvaluation
from eduintelligent.evaluation.config import PROJECTNAME
from eduintelligent.evaluation import evaluationMessageFactory as _
from eduintelligent.evaluation.content.evaluation import Evaluation
from eduintelligent.evaluation.content.schemas import quiz_schema, message_schema

### SCORM ###
from eduintelligent.sco.scorm.scormapi import ScormAPI
from eduintelligent.sco.scorm.track import TrackingStorage
from eduintelligent.sco.scorm.tracking import timeStamp2ISO


QuizFolderSchema = folder.ATFolderSchema.copy() + quiz_schema.copy() + message_schema.copy()

QuizFolderSchema['title'].storage = atapi.AnnotationStorage()
QuizFolderSchema['description'].storage = atapi.AnnotationStorage()

finalizeATCTSchema(QuizFolderSchema, folderish=True, moveDiscussion=False)
hideMetadataSchema(QuizFolderSchema, excludeFromNav=True)


class Quiz(Evaluation):
    """Contains multiple questions.
    """
    implements(IQuiz, IEvaluation)
    
    portal_type = "Quiz"
    _at_rename_after_creation = True
    schema = QuizFolderSchema
    
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    def getMaxOpportunityTest(self):
        return 100
    
    def getMaxTimeResponseTest(self):
        return 60
    
    def getMinScoreGrade(self):
        return 101
    
atapi.registerType(Quiz, PROJECTNAME)
