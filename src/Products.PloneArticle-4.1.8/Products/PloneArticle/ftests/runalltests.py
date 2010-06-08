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
# $Id: runalltests.py 5779 2007-01-21 17:41:41Z roeder $

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py')) 
	
from funittest.texttestrunner import TextTestRunner
from funittest import load_model
load_model("PloneArticle", "plonearticle")

import test_add_file
import test_add_link
import test_add_image
import test_browse_image
import test_delete_file

def suite():
    return unittest.TestSuite((
        unittest.makeSuite(test_add_file.TestAddFile),
        unittest.makeSuite(test_add_link.TestAddLink),
        unittest.makeSuite(test_add_image.TestAddImage),
        unittest.makeSuite(test_browse_image.TestBrowseImage),
        unittest.makeSuite(test_delete_file.TestDeleteFile),
        ))
        
if __name__ == "__main__":
    result = TextTestRunner(verbosity=2).run(suite())
    sys.exit(not result.wasSuccessful())
