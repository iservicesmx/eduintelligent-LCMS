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

__docformat__ = 'restructuredtext'


# articles have a private version attribute (integer type) starting from 0
#
# Each release including a change in article content type must be appended here
#
# WARNING: NEVER REMOVE ANY ENTRY IN THIS LIST.
#          ALWAYS ADD A NEW VERSION AT THE END (APPEND)
__VERSIONS = [
    '4.0.0-beta4',
    ]

# __VERSIONS[idx] = version_string (i.e, '4.0.0beta4')
# VERSIONS[version_string] = idx
VERSIONS = dict([(__VERSIONS[idx], idx) for idx in range(len(__VERSIONS))])

CURRENT_ARTICLE_VERSION = VERSIONS[__VERSIONS[-1]]

def getArticleVersionFor(version):
    return VERSIONS.get(version, None)

def getArticleVersionStringFor(version_num):
    return __VERSIONS[version_num]

__all__ = ('CURRENT_ARTICLE_VERSION', 'getArticleVersionFor',
           'getArticleVersionStringFor')
