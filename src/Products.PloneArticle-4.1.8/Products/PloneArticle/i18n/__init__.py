# -*- coding: utf-8 -*-
## Product description
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
# from CMFPlone 2.5
#
# Import "ArticleMessageFactory as _" to create message ids in the plonearticle
# domain
# Zope 3.1-style messagefactory module BBB: Zope 2.8 / Zope X3.0
try:
    from zope.i18nmessageid import MessageFactory
except ImportError:
    from messagefactory_ import ArticleMessageFactory, ModelMessageFactory
else:
    ArticleMessageFactory = MessageFactory('plonearticle')
    ModelMessageFactory = MessageFactory('plonearticle-model')
