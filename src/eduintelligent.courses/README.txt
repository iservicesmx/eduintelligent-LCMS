eduintelligent.courses Package Readme
======================================

Structural Overview
--------------------

This package contains code to create the ``Course Folder``. This folderish object
and can contain ``Course`` objects. Each ``Course`` object has the following
structure:
  * A *Lessons Folder** which can contain any number of ``PloneArticleMultiPage``
    objects. It's content-type is ``Lessons``.
  * A **Ploneboard** forum for online discussion.
  * Five ``CourseContent`` folderish objects that serve as special containers:
    - **exams** folder which can only contain ``ExamContent`` objects.
    - *quizzes** folder which can only contain ``QuizContent`` objects.
    - **polls** folder which can only contain ``PlonePopoll`` and ``Survey`` objects.
    - **faq** folder which can only contain ``FaqFolder`` and ``FaqEntry``  objects.
    - **files** folder which can only contain any kind of objects such as folders,
      images, PDF Files, etc..


It provides the following content-types:

  * **Course Folder**: This is the main container of Course folders.
  * **Course**: The container of all the course structure.
  * **Lessons**: The container for ``PloneArticleMultiPage`` objects. This
    content-type should be replaced by ``CourseContent``.
  * **CourseContent**: A General purpose container. We use GS to provide different
    alias.
  * **ExamContent**: Folderish item which can only contain 
  * QuizContent
  * PollContent


Dependencies:
PloneGlossary
Chat
PloneBoard
PlonePopoll
PloneSurvey
