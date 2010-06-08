# -*- coding: utf-8 -*-

from Products.Archetypes import atapi
from Products.validation import V_REQUIRED

from eduintelligent.evaluation import evaluationMessageFactory as _
from field import AnswerField
from widget import AnswerWidget

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget

###########################################################
# Quiz
###########################################################
quiz_schema = atapi.Schema((
    atapi.BooleanField("randomOrder",
                accessor='isRandomOrder',
                required=False,
                default=True,
                storage=atapi.AnnotationStorage(),
                widget=atapi.BooleanWidget(
                    label=_(u'Randomize Question Order'),
                    description=_(u'Check this box if you want the questions '
                                    u'in this container to appear in a different, random '
                                    u'order for each candidate. Otherwise the same order '
                                    u'as in the &quot;contents&quot;-view will be used.'),
                ),
    ),
    atapi.IntegerField("numberOfRandomQuestions",
            required=False,
            default=-1,
            storage=atapi.AnnotationStorage(),
            widget=atapi.IntegerWidget(
                label=_(u'Number of Random Questions'),
                description=_(u'The number of questions which are randomly '
                                u'selected when a new quiz is '
                                u'generated for a student. (This only works if '
                                u'&quot;Randomize Question Order&quot; '
                                u'is checked.) A value &lt;= 0 means that all '
                                u'questions will be used.'),
            ),
    ),
    atapi.BooleanField('BadResults',
         default=True,
         accessor='viewBadResults',
         storage=atapi.AnnotationStorage(),
         widget = atapi.BooleanWidget(
             label=_(u'Show incorrect answers'),
         )
     ),
 
))

###########################################################
# Exam Schema
###########################################################
exam_schema = atapi.Schema((
    atapi.IntegerField("maxTimeResponseTest",
            required=False,
            default=40,
            storage=atapi.AnnotationStorage(),
            widget=atapi.IntegerWidget(
                label=_(u'Exam Time'),
                description=_(u'Maximun time in minutes for the user to complete the exam'),
            ),
    ),
    atapi.DateTimeField('initDate',
        required = 1,
        searchable = 0,
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u'Start Date'),
            description=_(u"Exam's start date"),
        ),
    ),
    atapi.DateTimeField('finishDate',
        required = 1,
        searchable = 0,
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u'End Date'),
            description= _(u"Exam's end date"),
        ),
    ),
    atapi.IntegerField("maxOpportunityTest",
            required=False,
            default=2,
            storage=atapi.AnnotationStorage(),
            widget=atapi.IntegerWidget(
                label=_(u'Opportunities to pass'),
                description=_(u'Maximum number of chances the user has in order tho pass the exam'),
            ),
    ),
    atapi.FloatField('minScoreGrade',
            required=False,
            default=90.0,
            storage=atapi.AnnotationStorage(),
            widget=atapi.DecimalWidget(
                label=_(u'Score to approve'),
                description=_(u'Minimun score to pass the exam'),
                )
    ),  
    atapi.ReferenceField('evaluationDependecy',
            relationship='evaluation_dependecy',
            allowed_types=('Exam',),
            multiValued=False,
            #keepReferencesOnCopy=True,
            storage=atapi.AnnotationStorage(),
            widget=ReferenceBrowserWidget(
                label=_(u'Referenced Evaluation'),
                description=_(u'Choose an exam that allow to take this exam'),
                ),
            ),
    
    
    )
)

###########################################################
# Schema for messaging?
###########################################################

message_schema = atapi.Schema((
    atapi.BooleanField('showMessages',
        schemata ="Messages",
        storage = atapi.AnnotationStorage(),
        widget = atapi.BooleanWidget(
            label=_(u'Show messages'),
            visible=0,
        )
     ),
    atapi.StringField('veryGoodScoreTitle',
         schemata="Messages",
         storage=atapi.AnnotationStorage(),
         widget=atapi.StringWidget(
             label=_('Very good score title'),
             visible=0,
        ),
    ),
    atapi.StringField('veryGoodScoreMessage',
         schemata="Messages",
         storage=atapi.AnnotationStorage(),
         widget=atapi.TextAreaWidget(
             label=_(u'Very good score message'),
             visible=0,
        ),
    ),
    atapi.StringField('goodScoreTitle',
         schemata="Messages",
         storage=atapi.AnnotationStorage(),
         widget=atapi.StringWidget(
             label=_(u'Good score title'),
             visible=0,
        ),
    ),
    atapi.StringField('goodScoreMessage',
         schemata="Messages",
         storage=atapi.AnnotationStorage(),
         widget=atapi.TextAreaWidget(
             label=_(u'Good score message'),
             visible=0,
        ),
    ),
    atapi.StringField('badScoreTitle',
         schemata="Messages",
         storage=atapi.AnnotationStorage(),
         widget=atapi.StringWidget(
             label=_(u'Bad score title'),
             visible=0,
        ),
    ),
    atapi.StringField('badScoreMessage',
         schemata="Messages",
         storage=atapi.AnnotationStorage(),
         widget=atapi.TextAreaWidget(
             label=_(u'Bad score message'),
             visible=0,
        ),
    ),
    atapi.StringField('veryBadScoreTitle',
         schemata="Messages",
         storage=atapi.AnnotationStorage(),
         widget=atapi.StringWidget(
             label=_(u'Very bad score title'),
             visible=0,
        ),
    ),
    atapi.StringField('veryBadScoreMessage',
         schemata="Messages",
         storage=atapi.AnnotationStorage(),
         widget=atapi.TextAreaWidget(
             label=_(u'Very bad score message'),
             visible=0,
        ),
    ),
))

###########################################################
# Base question Schema
###########################################################

base_question_schema = atapi.Schema((
    # By using the name 'image' we can have the image show up in preview
    # folder listings for free
    atapi.ImageField('qimage',
        required=False,
        languageIndependent=True,
        storage=atapi.AnnotationStorage(),
        swallowResizeExceptions=True,
        max_size='no',
        sizes={'large'   : (600, 600),
               'preview' : (400, 400),
               'mini'    : (200, 200),
               'thumb'   : (128, 128),
               },
        validators=(('isNonEmptyFile', V_REQUIRED),
                    ('checkImageMaxSize', V_REQUIRED)),
        widget=atapi.ImageWidget(label= _(u"Image"),
                                 description = _(u"An image for this question (The image size must not be greater than 400x400 px)"),
                                 show_content_type = False,),
        ),

    atapi.IntegerField("maxTimeResponseQuestion",
             required=False,
             default=70,
             storage=atapi.AnnotationStorage(),
             widget=atapi.IntegerWidget(
                 label=_(u'Time of response (Seconds)'),
                 description=_(u'Maximum time, in seconds, the user has in order to answer the question'),
            ),
        ),       
    atapi.FloatField("weighting",
             required=True,
             default=1.0,
             storage=atapi.AnnotationStorage(),
             widget=atapi.DecimalWidget(
                 label=_(u'Weight'),
                 description=_(u'The weight factor of this question'),
            ),
        ),       


))

###########################################################
# Schema for QuestionChoice
###########################################################
questionchoice_schema = atapi.Schema((
    AnswerField('answers',
        required = True,
        storage=atapi.AnnotationStorage(),
        widget=AnswerWidget(
            label=_('Answers'),
            description=_("Defines how many possible answers are there for this question")
        ),
    ),
    atapi.BooleanField('AnswersRandomOrder',
        default=False,
        accessor='viewAnswersRandomOrder',
        storage=atapi.AnnotationStorage(),
        widget = atapi.BooleanWidget(
             label=_(u'Show in random order'),
             description=_(u'Show the answers in random order'),
          )
      ),
))
###########################################################
#
###########################################################

