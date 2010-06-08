#
#  Copyright (c) 2007 Helmut Merz helmutm@cy55.de
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

"""
loops tracking interface definitions.

$Id: interfaces.py 2019 2007-09-09 19:45:54Z helmutm $
"""

from zope.interface import Interface, Attribute
from zope import schema

from eduintelligent.database import databaseMessageFactory as _


# Database connectivity

class IDatabaseSettings(Interface):
    """Database connection settings.
    """

    drivername = schema.ASCIILine(title=_(u"Driver name"),
                                  description=_(u"The database driver name"),
                                  default='mysql',
                                  required=True)

    hostname = schema.ASCIILine(title=_(u"Host name"),
                                description=_(u"The database host name"),
                                default='localhost',
                                required=True)

    port = schema.Int(title=_(u"Port number"),
                      description=_(u"The database port number. Leave blank to use the default."),
                      required=False)

    username = schema.ASCIILine(title=_(u"User name"),
                                description=_(u"The database user name"),
                                required=True)

    password = schema.Password(title=_(u"Password"),
                                description=_(u"The database password"),
                                required=False)

    database = schema.ASCIILine(title=_(u"Database name"),
                                description=_(u"The name of the database on this server"),
                                required=True)