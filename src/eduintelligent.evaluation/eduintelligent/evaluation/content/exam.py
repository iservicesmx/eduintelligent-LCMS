# -*- coding: utf-8 -*-
"""Definition of the Exam content type.
"""

from zope.interface import implements
from Products.Archetypes import atapi

from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from eduintelligent.evaluation.utility import hideMetadataSchema
from eduintelligent.evaluation.interfaces import IExam, IEvaluation
from eduintelligent.evaluation.config import PROJECTNAME
from eduintelligent.evaluation import evaluationMessageFactory as _
from eduintelligent.evaluation.content.evaluation import Evaluation
from eduintelligent.evaluation.content.schemas import quiz_schema, exam_schema, message_schema

ExamFolderSchema = folder.ATFolderSchema.copy() + quiz_schema.copy() + exam_schema.copy() + message_schema.copy()
ExamFolderSchema['title'].storage = atapi.AnnotationStorage()
ExamFolderSchema['description'].storage = atapi.AnnotationStorage()

finalizeATCTSchema(ExamFolderSchema, folderish=True, moveDiscussion=False)
hideMetadataSchema(ExamFolderSchema, excludeFromNav=True)

class Exam(Evaluation):
    """Contains multiple questions.
    """
    implements(IExam, IEvaluation)
    
    portal_type = "Exam"
    _at_rename_after_creation = True
    schema = ExamFolderSchema
    
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    


atapi.registerType(Exam, PROJECTNAME)
