# -*- coding: utf-8 -*-
## PloneArticle
## 
## Copyright (C) 2006 Ingeniweb

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING. If not, write to the
## Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

#
# from CMFPlone 2.5
#
# CMFPlone/LICENCE.txt:
#   The Plone Content Management System is built on the Content 
#   Management Framework (CMF) and the Zope Application Server.
#   Plone is copyright 2000-2006 Plone Foundation et al.
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
# Zope 3.1-style messagefactory module for Zope <= 2.9 (Zope 3.1)
#

# BBB: Zope 2.8 / Zope X3.0

from zope.i18nmessageid import MessageIDFactory
msg_factory = MessageIDFactory('plonearticle')

def ArticleMessageFactory(ustr, default=None, mapping=None):
    message = msg_factory(ustr, default)
    if mapping is not None:
        message.mapping.update(mapping)
    return message

model_msg_factory = MessageIDFactory('plonearticle-model')

def ModelMessageFactory(ustr, default=None, mapping=None):
    message = model_msg_factory(ustr, default)
    if mapping is not None:
        message.mapping.update(mapping)
    return message
