# -*- coding: utf-8 -*-
## PloneArticle
## A Plone document incorporating images, attachments and links, whith a free choice of layout.
## Copyright (C)2006 Ingeniweb

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
# $Id: framework.py 2163 2006-10-27 13:23:55Z roeder $
##############################################################################
#
# ZopeTestCase 
#
# COPY THIS FILE TO YOUR 'tests' DIRECTORY.
#
# This version of framework.py will use the SOFTWARE_HOME
# environment variable to locate Zope and the Testing package.
#
# If the tests are run in an INSTANCE_HOME installation of Zope,
# Products.__path__ and sys.path with be adjusted to include the
# instance's Products and lib/python directories respectively.
#
# If you explicitly set INSTANCE_HOME prior to running the tests,
# auto-detection is disabled and the specified path will be used 
# instead.
#
# If the 'tests' directory contains a custom_zodb.py file, INSTANCE_HOME
# will be adjusted to use it.
#
# If you set the ZEO_INSTANCE_HOME environment variable a ZEO setup 
# is assumed, and you can attach to a running ZEO server (via the 
# instance's custom_zodb.py).
#
##############################################################################
#
# The following code should be at the top of every test module:
#
# import os, sys
# if __name__ == '__main__':
#     execfile(os.path.join(sys.path[0], 'framework.py'))
#
# ...and the following at the bottom:
#
# if __name__ == '__main__':
#     framework()
#
##############################################################################

__version__ = '0.2.3'

# Save start state
#
__SOFTWARE_HOME = os.environ.get('SOFTWARE_HOME', '')
__INSTANCE_HOME = os.environ.get('INSTANCE_HOME', '')

if __SOFTWARE_HOME.endswith(os.sep):
    __SOFTWARE_HOME = os.path.dirname(__SOFTWARE_HOME)

if __INSTANCE_HOME.endswith(os.sep):
    __INSTANCE_HOME = os.path.dirname(__INSTANCE_HOME)

# Find and import the Testing package
#
if not sys.modules.has_key('Testing'):
    p0 = sys.path[0]
    if p0 and __name__ == '__main__':
        os.chdir(p0)
        p0 = ''
    s = __SOFTWARE_HOME
    p = d = s and s or os.getcwd()
    while d:
        if os.path.isdir(os.path.join(p, 'Testing')):
            zope_home = os.path.dirname(os.path.dirname(p))
            sys.path[:1] = [p0, p, zope_home]
            break
        p, d = s and ('','') or os.path.split(p)
    else:
        print 'Unable to locate Testing package.',
        print 'You might need to set SOFTWARE_HOME.'
        sys.exit(1)

import Testing, unittest
execfile(os.path.join(os.path.dirname(Testing.__file__), 'common.py'))

# Include ZopeTestCase support
#
if 1:   # Create a new scope

    p = os.path.join(os.path.dirname(Testing.__file__), 'ZopeTestCase')

    if not os.path.isdir(p):
        print 'Unable to locate ZopeTestCase package.',
        print 'You might need to install ZopeTestCase.'
        sys.exit(1)

    ztc_common = 'ztc_common.py'
    ztc_common_global = os.path.join(p, ztc_common)

    f = 0
    if os.path.exists(ztc_common_global):
        execfile(ztc_common_global)
        f = 1
    if os.path.exists(ztc_common):
        execfile(ztc_common)
        f = 1

    if not f:
        print 'Unable to locate %s.' % ztc_common
        sys.exit(1)

# Debug
#
print 'SOFTWARE_HOME: %s' % os.environ.get('SOFTWARE_HOME', 'Not set')
print 'INSTANCE_HOME: %s' % os.environ.get('INSTANCE_HOME', 'Not set')
sys.stdout.flush()

