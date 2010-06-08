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
from Products import PloneArticle as PRODUCT
import os.path

version = PRODUCT.__version__
modname = PRODUCT.__name__

# (major, minor, revision)
# i.e 4.0.0-beta4 CVS/SVN (UNRELEASED) => (4, 0, 0, 'beta2')
ver_tup = version.split(' ')
vers = ver_tup[0]
major, minor, suffix =  vers.split('.')
suffix = suffix.split('-')
bugfix = suffix[0]
release = len(suffix) > 1 and suffix[1] or ''
numversion = (int(major), int(minor), int(bugfix), release)

license     = 'GPL'
copyright   = '''(c) 2006 Ingeniweb'''

author      = 'Ingeniweb <support@ingeniweb.com>'
author_email= 'support@ingeniweb.com'

short_desc  = 'Article content type for Plone'
long_desc   = '''
'''

copyright_text = '''
'''

web         = 'http://plone.org/products/plonearticle'
ftp         = ''
mailing_list= ''
bugtracker  = 'http://sourceforge.net/tracker/?atid=541550&group_id=74634'
