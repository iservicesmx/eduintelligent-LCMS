############
PloneArticle
############

The Ingeniweb team proudly presents the fourth generation of their
star product.

About
#####

A Plone document including images, attachments and links, with a
free choice of layout.

Requirements
############

Plone 3.0 and more

Recommanded add-ons
###################

AttachmentField
===============

Have your embedded office files indexed with the magic of
AttachmentField.

http://plone.org/products/attachmentfield

FCKeditor
=========

FCKeditor for Plone is a WYSIWYG editor you may prefer to Kupu. It
comes with nice PloneArticle dedicated features: an images and files
browser that finds the PloneArticle embedded images and files, images
and files uploading directly in the PloneArticle.

http://plone.org/products/fckeditor

Install
#######

In your instance :

* using buildout :
  
  - just add Products.PloneArticle in your instance eggs list of your buildout.cfg
  
* using easy_install, at prompt :
  
  - easy_install Products.PloneArticle
  
* in a "classical" zope instance
  
  - unflate the archive Products.PloneArticle.xxxx.zip
  
  - Copy only the directory named "PloneArticle" inside the unpacked "Products.PloneArticle" directory
    Paste it to your zope instance Products dir.  
  
In your Plone site :  

* Use the quickinstaller on your Plone site(s)

* Go to the PloneArticle preferences configlet and tweak it in
  conformance with your site policy.


Configure
#########

General
=======

PloneArticle comes with a configuration panel to tweak most harmless
features (available models, file/image/link types). You can limit the
size (in bytes) for uploaded images and files.

CMFEditions support
===================

Open as site Manager http://_your_site_/versioning_config_form in your
browser (yes, there's no link from control panel portet in Plone
3.0.3!), and activate versioning for PloneArticle. Optionally select
desired policies.

Be aware that versioning is open to bloat your ZODB as long as
CMFEditons uses it as repository back-end.


Wicked support
==============

PloneArticle is by default wicked aware. As usual, you just need to
type `((some word))` to have it behave like a wiki word. If you don't
want this behaviour, you just need to edit `implements.zcml` and
remove or comment the XML elements with `wicked` namespace.

Sorry for this complex stuff but there's no easy way to do this
TTW or through a config file.


License
#######

Copyright (c) 2007 Ingeniweb SAS

This software is subject to the provisions of the GNU General Public
License, Version 2.0 (GPL).  A copy of the GPL should accompany this
distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY,
AGAINST INFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE

More details in the ``LICENSE`` file included in this package.

Further documentation
#####################

Please search and read from the ``doc`` directory. You'll find all you
need if you want to subclass the PloneArticle or add your personal
views.

Testing
#######

Please read ``tests/README.txt' for unit tests and
``ftests/README.txt`` for functional tests.

Credits
#######

* Engineering by `the Ingeniweb team <http://www.ingeniweb.com>`_

* Slovenian translation by Matjaz Jeran (matematik) <matjaz.jeran@amis.net>

* Brasilian Portugese translation by Erico Andrei <erico@simplesconsultoria.com.br>

* German translation by Andreas Kaiser <kaiser@xo7.de>

* Russian translation by Roman Susi <roman.susi@hexagonit.fi>

SVN repository
##############

https://svn.plone.org/svn/collective/Products.PloneArticle

Download
########

You may find newer versions of PloneArticle at
http://plone.org/products/plonearticle

Support
#######

Before asking for support, please make sure that your problem is not
described in the documentation that ships with PloneArticle (this file
and the ones from the ``doc`` directory).

* `Mail to Ingeniweb support <mailto:support@ingeniweb.com>`_ in english or french.

* `Report bugs in english only
  <http://sourceforge.net/tracker/?atid=541550&group_id=74634>`_ if it
  has not already been reported.

`Donations are welcome for new features <http://sourceforge.net/project/project_donations.php?group_id=74634>`_
