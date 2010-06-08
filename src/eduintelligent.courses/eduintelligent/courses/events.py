# -*- coding: utf-8 -*-
#
# File: eduTrainingCenter/events.py
#
# Copyright (c) 2007 Erik Rivera Morales <erik@ro75.com>
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

"""
$Id$
"""

__author__ = """Erik Rivera Morales <erik@ro75.com>"""
__docformat__ = 'reStructuredText'
__licence__ = 'GPL'

from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from Products.ATContentTypes.lib import constraintypes


from eduintelligent.courses.interfaces import ICourse
from eduintelligent.courses import coursesMessageFactory as _

def makeItem(context, cid, ctype, title, description, publish=True):
    """makeItem utility : Item Constructor
    
     @param context : Context's Object ID.
     @param cid : The id of the new Item.
     @param ctype : The object type of the new Item.
     @param title : The title of the new Item.
     @param description : The description of the object being created.
     @param publish : Set the new item's state to 'Published'.
    
     reindexes the object at the end
    """
    if cid not in context.objectIds():
        wftool = getToolByName(context, "portal_workflow")
        _createObjectByType(ctype,context,cid)
        obj = context[cid]
        obj.setTitle(obj.translate(
                msgid='%s_title'%(cid),
                domain='eduintelligent.courses',
                default=title))
        obj.setDescription(obj.translate(
                        msgid='%s_description'%(cid),
                        domain='eduintelligent.courses',
                        default=description)) 
        obj.unmarkCreationFlag() #??????
        
        if publish:
            if wftool.getInfoFor(obj, 'review_state') != 'published':
                wftool.doActionFor(obj, 'publish')
        
        obj.reindexObject()
        return obj


def createCourse(obj, event):
    """
    This is a callback function for the IObjectInitializedEvent.
    
    This function is called when a course folder has been created.
    
    The ZCML call is:
        <subscriber
            for=".interfaces.ICourse
                Products.Archetypes.interfaces.IObjectInitializedEvent"
            handler=".events.createCourse"
        />
    
    """
    context = ICourse(obj)
    # Make a Lessons folder
    makeItem(context, 
             'lessons',
             'Lessons',
             'Modules',
             'Insert content and configure as necesary')
    # Make Forum
    makeItem(context, 
             'forum',
             'Ploneboard',
             'Foro',
             'Necesita configurar el foro', 
             publish=False)
    # Make Tests
    makeItem(context, 
             'exams',
             'ExamContent',
             'Exámenes',
             'Exámenes del curso')
    #obj.setConstrainTypesMode(constraintypes.ENABLED)        
    #obj.setLocallyAllowedTypes(['Exam'])
    #obj.setImmediatelyAddableTypes(['Exam'])
    #obj.setLayout('view_exams')
    #obj.reindexObject()
    
    # Make Quizzes
    makeItem(context, 
             'quizzes',
             'QuizContent',
             'Quizzes',
             'Quizes de los cursos')
    # obj.setConstrainTypesMode(constraintypes.ENABLED)        
    # obj.setLocallyAllowedTypes(['Quiz'])
    # obj.setImmediatelyAddableTypes(['Quiz'])
    # obj.setLayout('view_quizzes')
    # obj.reindexObject()
    
    # Make Polls
    makeItem(context, 
             'polls',
             'PollContent',
             'Encuestas',
             'Encuestas del Curso')
    # obj.setConstrainTypesMode(constraintypes.ENABLED)        
    # obj.setLocallyAllowedTypes(['PlonePopoll'])
    # obj.setImmediatelyAddableTypes(['PlonePopoll'])
    # obj.setLayout('view_polls')
    # obj.reindexObject()
    
    # Make Chat
    #makeItem(context, 'chat','Chat',_('Chat'),_('Course Chat'))
    
    # Make Glossary
    makeItem(context, 
             'glossary',
             'PloneGlossary',
             'Glosario',
             'Glosario del Curso')
    
    # Make Faq
    makeItem(context, 
             'faq',
             'FaqFolder',
             'Faq',
             'Faq del Curso')
    
    # Make Files
    makeItem(context, 
             'files',
             'Resources',
             'Recursos',
             'Carpeta contenedora de archivos del curso')
    
    # Make Bibliography
    makeItem(context, 
             'bibliography',
             'Biblio',
             u'Bibliografía',
             u'Para utilizar la bibliografía debe personalizar la categorías en la pestaña editar')
    
    context.reindexObject()
    

def editCourse(obj, event):
    """
    This is a callback function for the IObjectEditedEvent.
    
    This function is called when a course folder has been edited.
    
        <subscriber
            for=".interfaces.ICourse
                Products.Archetypes.interfaces.IObjectEditedEvent"
            handler=".events.editCourse"
        />
    
    """
    context = ICourse(obj)
    #Set the instructors
    instructors = context.getLocalRoles('Manager')
    context.setInstructor(instructors)
    #print "editCourse-instructor ",instructors
    
    #Register all the users
    registered = len(context.getRegisteredStudents())
    context.setRegistered(registered)
    #print "editCourse-getRegisteredStudents ", registered 
