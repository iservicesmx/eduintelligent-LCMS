# -*- coding: utf-8 -*-
#
# File: Book.py
#
# Copyright (c) 2007 by ['Juan Ramon Lopez Beristain']
# Generator: ArchGenXML Version 2.0-alpha svn/development
#            http://plone.org/products/archgenxml
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

__author__ = """Juan Ramon Lopez Beristain <ramon@ro75.com>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.Archetypes.public import DisplayList

try:
    from Products.LinguaPlone.public import *
except ImportError:
    HAS_LINGUAPLONE = False
else:
    HAS_LINGUAPLONE = True

from zope import interface
from zope.interface import implements
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.eduBiblio.interfaces import IBook
from Products.eduBiblio.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((
    StringField(
        name="booktype",
        required                = True,
        vocabulary=typebooks,
        widget=SelectionWidget(
            i18n_domain='eduBiblio',
            label='Typebook',
            label_msgid='eduBiblio_label_type',
            description_msgid = "eduBiblio_booktype",
            description       = "The type to the book.",
        )
    ),
    LinesField(
        name="author",
        required                = False,
        widget                  = LinesWidget(
            i18n_domain       = "eduBiblio",
            label             = "Author",
            label_msgid       = "eduBiblio_author_label",
            description_msgid = "eduBiblio_author",
            description       = "The Author to the book.",
            )
    ),
	IntegerField("datepub",
		required                = False,
		widget                  = IntegerWidget(
		    i18n_domain       = "eduBiblio",
		    label             = "Year of Publication",
		    label_msgid       = "eduBiblio_fchpub_label",
		    description_msgid = "eduBiblio_fchpub",
		    description       = "The Year Public to the book.",
		    )
		),
	StringField("editorial",
		required                = False,
		widget                  = StringWidget(
			i18n_domain       = "eduBiblio",
			label             = "Editorial",
			label_msgid       = "eduBiblio_editoria_label",
			description_msgid = "eduBiblio_editoria",
			description       = "The Editorial of the book.",
			)
		),		

    StringField(
        required                = False,
        name='isbn',
        widget=StringWidget(
            i18n_domain='eduBiblio',
            label='Isbn',
            label_msgid='eduBiblio_isbn_label',
            description_msgid = "eduBiblio_isbn",
			description       = "The Isbn to the book.",
        )
    ),

    StringField(
        required                = False,
        name='link',
        widget=StringWidget(
            label='Link',
            label_msgid='eduBiblio_link_label',
            i18n_domain='eduBiblio',
            description_msgid = "eduBiblio_link",
			description       = "The link to the book.",
        )
    ),

    ImageField(
        required                = False,
        name='preview',
        widget=ImageWidget(
            i18n_domain='eduBiblio',
            label='Preview',
            label_msgid='eduBiblio_preview_label',
            description_msgid = "eduBiblio_preview",
			description       = "The Img Preview to the book.",
        ),
        storage=AttributeStorage()
    ),

    LinesField(
        required                = True,
        name='category',
        vocabulary='getCategories',
        widget=MultiSelectionWidget(
            i18n_domain='eduBiblio',
            label='Category',
            label_msgid='eduBiblio_label_category',
            description_msgid = "eduBiblio_category",
			description       = "The category to the book.",
        ),
        multiValued=1
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Book_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema
for field in Book_schema.fields():
    if field.isMetadata:
        field.schemata = 'default'
        field.widget.visible = False

DescField = Book_schema['description']
DescField.widget.visible = True

class Book(BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(IBook)
    meta_type = 'Book'
    _at_rename_after_creation = True

    schema = Book_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('getCategories')
    def getCategories(self):
        """
        """
        parent = self.aq_inner.aq_parent
        print "el padre es:", type(parent)
        catego = parent.getCategory()
        print "categorias:   ", catego
        
        return catego
        
    def getTypebooksName(self):
        """
        get the label by key
        """
        return typebooks.getValue(self.getBooktype())
        

registerType(Book, PROJECTNAME)
# end of class Book

##code-section module-footer #fill in your manual code here
##/code-section module-footer



