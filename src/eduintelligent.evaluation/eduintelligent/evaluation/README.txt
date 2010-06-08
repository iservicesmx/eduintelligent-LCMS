eduintelligent.extrastats
=========================
Introduction
-------------

This is an add-on Plone product that extracts information from TrainingCenters, 
Courses and Evaluations (Including Exams and Quizes) and calculates required 
Statistics.

The eduintelligent.evaluation product already provides the following information
regarding Evaluations (Exams and Quiz):

+ Per-user Evaluation score
+ A ssign an extra score (manually) on a per-evaluation, per-user basis.
+ Per-user Evaluation average from normal and extra-score.

Additionaly, this product will provide 

+ Top 3 averages on normal score and extra score.
+ A list of all failed evaluations (less than 85), for both normal score and 
  extra score.
+ General Average from all users in a Training Center.
+ General Average from all users in a Group, Division or Region (or equivalent). 
  Sort descending and mark the highest average.
+ Display, on a per-evaluation basis, the questions that had the most erroneous 
  answers.

Dependencies
============


This product was developed and only tested on 3.3+.

Requires all the dependencies for the eduIntelligent LCMS platform.


Installation
------------

Assuming that you are using zc.buildout and the plone.recipe.zope2instance 
recipe to manage your project, proceed this way:

Add eduintelligent.extrastats to the list of eggs to install, e.g.:
::
  [buildout]
    ...
    eggs =
      ...
      eduintelligent.extrastats

Re-run buildout, e.g. with:
::
  $ ./bin/buildout

Then you can install the product into your Plone site from the Plone control 
panel.

