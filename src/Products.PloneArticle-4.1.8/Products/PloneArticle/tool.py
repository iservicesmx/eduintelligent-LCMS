# -*- coding: utf-8 -*-
## Copyright (C) 2005-2007 Ingeniweb

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
"""
This module contains the tool of PloneArticle product
"""

# Python imports
import os, sys, traceback
from StringIO import StringIO
import logging
from types import StringType, ListType, TupleType
import re
from cgi import escape

# Zope imports
import transaction
from Globals import InitializeClass
from ZODB.POSException import ConflictError
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
from OFS.Image import File, Image
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

# CMF imports
from Products.CMFCore.utils import UniqueObject, getToolByName, registerToolInterface
from Products.CMFCore import permissions as CCP

# Plone imports
from Products.CMFPlone import PloneMessageFactory

# Archetypes imports
from Products.Archetypes.public import MinimalSchema, Schema, ImageField, BaseUnit

# Products imports
from Products.PloneArticle import LOG
from Products.PloneArticle.config import PLONEARTICLE_TOOL
from Products.PloneArticle.interfaces import IPloneArticle, IPloneArticleTool, IBaseInnerContentProxy
from Products.PloneArticle.browser.interface import IPloneArticleModelView
from Products.PloneArticle.proxy import BaseInnerContentProxy
from Products.PloneArticle.field import BaseInnerContentField
from Products.PloneArticle.model import getModelRegistry
from Products.PloneArticle import utils
from Products.PloneArticle.i18n import ArticleMessageFactory

# Check AttachmentField product installation
USE_ATTACHMENT_FIELD = True

try:
    from Products.AttachmentField import AttachmentField
except:
    USE_ATTACHMENT_FIELD = False

# Parse thumbnail id
THUMBNAIL_RE = re.compile(r'(?P<field_name>[a-zA-Z0-9]*)x(?P<width>\d*)x(?P<height>\d*).(?P<ext>[a-zA-Z0-9]*)')

try:
    import PIL.Image
except ImportError:
    # no PIL, no scaled versions!
    HAS_PIL = False
else:
    HAS_PIL = True


_upgradePaths = {}

def registerUpgradePath(oldversion, newversion, function):
    """ Basic register func """
    _upgradePaths[oldversion.lower()] = [newversion.lower(), function]


class PloneArticleTool(UniqueObject, SimpleItem):
    """
    Tool for PloneArticle
    """

    plone_tool = True
    id = PLONEARTICLE_TOOL
    title = "Misc utilities for PloneArticle"
    meta_type = 'PloneArticleTool'

    _numversion = ()
    _version = ''

    manage_options = SimpleItem.manage_options

    security = ClassSecurityInfo()

    # structure:{'PloneArticle': {'image': ['Image'], ...}, ...}
    referenceable_types = {}

    migrationWwwPath = os.path.join(os.path.dirname(__file__), 'www', 'migration')

    manage_options += (
        ({'label' : 'Migration',
          'action' : 'migration'
          },)
    )

    migration = PageTemplateFile(migrationWwwPath)
    security.declareProtected(CCP.ManagePortal, 'migration')


    security.declarePublic('listArticleImplementers')
    def listArticleImplementers(self):
        """
        Return all portal types which support IPloneArticle
        """
        at = getToolByName(self, 'archetype_tool')
        return at.listPortalTypesWithInterfaces((IPloneArticle,))

    security.declarePublic('getModelRegistry')
    def getModelRegistry(self):
        """
        """
        return getModelRegistry()

    security.declarePublic('getModelIcon')
    def getModelIcon(self, model_id):
        """
        """
        registry = getModelRegistry()
        model = registry.get(model_id, None)
        if model is None:
            return "pa_default_model.gif"
        return model.icon

    security.declarePublic('getModelsForType')
    def getEnabledModelsForType(self, portal_type):
        """
        Return the set of templates availables as views for portal_type, and the
        default_view .

        @param portal_type: a string or a portal_type object
        """
        if isinstance(portal_type, basestring):
            pt = getToolByName(self, 'portal_types')
            portal_type = pt.getTypeInfo(portal_type)

        return (portal_type.view_methods, portal_type.default_view)

    security.declareProtected(CCP.ManagePortal, 'setEnabledModelsForType')
    def setEnabledModelsForType(self, portal_type, templates,
                                default_view=None):
        """
        Change the set of templates availables as views for portal_type.

        @param portal_type: a string or a portal_type object
        """
        if (not type(templates) in (ListType, TupleType)) \
               or len(templates) == 0:
            return

        if isinstance(portal_type, basestring):
            pt = getToolByName(self, 'portal_types')
            portal_type = pt.getTypeInfo(portal_type)

        if default_view not in templates:
            # if we don't do that CMFDynamicviewFTI will raise ValueError
            # we must give a valid default view
            default_view = templates[0]

        portal_type.manage_changeProperties(view_methods=tuple(templates),
                                            default_view=default_view)


    security.declareProtected(CCP.ManagePortal, 'setOptionsForType')
    def setOptionsForType(self, portal_type_name, field_name, arg_name, **args):
        """
            Set various options in FTIs properties.
        """
        pt = getToolByName(self, 'portal_types')
        portal_type = pt.getTypeInfo(portal_type_name)
        portal_type.manage_changeProperties(**args)
        updates = {
            portal_type_name: {
                field_name: args[arg_name]
            }
        }
        self.updateReferenceableTypes(updates=updates)


    security.declarePublic('getAllAvailableReferenceableImageTypes')
    def getAllAvailableReferenceableImageTypes(self):
        from Products.PloneArticle.proxy.imageinnercontent import ImageInnerContentProxy
        return utils.getAllAvailableReferenceableTypes(self, ImageInnerContentProxy)

    security.declarePublic('getAllAvailableReferenceableLinkTypes')
    def getAllAvailableReferenceableLinkTypes(self):
        from Products.PloneArticle.proxy.linkinnercontent import LinkInnerContentProxy
        return utils.getAllAvailableReferenceableTypes(self, LinkInnerContentProxy)

    security.declarePublic('getAllAvailableReferenceableAttachmentTypes')
    def getAllAvailableReferenceableAttachmentTypes(self):
        from Products.PloneArticle.proxy.fileinnercontent import FileInnerContentProxy
        return utils.getAllAvailableReferenceableTypes(self, FileInnerContentProxy)


    security.declarePublic('listModels')
    def listModels(self,):
        """
        Return a sorted list of all registered models
        """
        registry = getModelRegistry()
        models = registry.values()
        models.sort()
        return models

    security.declarePublic('getReferenceablePortalTypesFor')
    def getReferenceablePortalTypesFor(self, proxy, field):
        """
        Return a list of portal types that this InnerProxy instance can
        reference.
        """
        assert(isinstance(proxy, BaseInnerContentProxy))
        assert(isinstance(field, BaseInnerContentField))

        article = proxy.getArticleObject()
        article_type = article.portal_type
        ref_types = self.referenceable_types

        if not ref_types.has_key(article_type):
            self.updateReferenceableTypes()
        proxy_dict = ref_types[article_type]
        return proxy_dict[field.getName()]

    security.declareProtected(CCP.ManagePortal, 'updateReferenceableTypes')
    def updateReferenceableTypes(self, updates={}, reset=False):
        """
        Update InnerProxy referenceables types structure. This structure is a dict:

        {'PloneArticle': {
                'files': ['File'],
                'images': ['Image', 'News Item'],
                'links': ['Favorite', 'Link']
                },
         'ContentUsingInnerFields': {...},
        }

        Without any param, this method will update this mapping, detecting new
        types/fields and preserving existing entries.

        @param updates: a dict like referenceable_types. Its entries will
        override default values (i.e constrain allowed types). Unsupported types
        for reference by the proxy will be ignored.

        @param reset: reset all mapping, allowing to reference all types
        supported by InnerProxies. If reset, the param 'updates' is ignored.
        """

        at = getToolByName(self, 'archetype_tool')
        ref_types_info = self.referenceable_types
        registered_types = at.listRegisteredTypes()
        registered_portal_types = [i['portal_type'] for i in registered_types]
        pa_types = at.listPortalTypesWithInterfaces([IPloneArticle,])
        proxy_types = at.listPortalTypesWithInterfaces([IBaseInnerContentProxy,])
        proxy_types = [fti.getId() for fti in proxy_types]

        for fti in pa_types:
            portal_type = fti.getId()
            idx = registered_portal_types.index(portal_type) #ValueError no idx
            ## this is the schema of the PA like object
            schema = registered_types[idx]['schema']

            if portal_type not in ref_types_info:
                ## this is the case when a new PA like type has just been installed
                ref_types_info[portal_type] = {}
            pti = ref_types_info[portal_type]

            pt_update = updates.get(portal_type, {})

            for field in schema.fields():
                field_name = field.getName()
                field_update = pt_update.get(field_name)

                ## I the two next tests, we will skip if field is not
                ## updated or reset
                if not isinstance(field, BaseInnerContentField):
                    ## this field is just a simple field, not a proxy, so no update
                    continue

                if (
                    not field_update ## we have no reference in the update table
                    and pti.has_key(field_name) ## a field already exist
                    and not reset ## we don't want to reset
                ):
                    continue

                ## we look for interfaces of inner types
                inner_pt = field.inner_portal_type
                inner_class_idx = registered_portal_types.index(inner_pt)
                inner_class = registered_types[inner_class_idx]['klass']

                ct = utils.getAllAvailableReferenceableTypes(self, inner_class)

                ## here we keep the old ones if reset is not wanted
                if field_update and not reset:
                    new_ct = [pt for pt in ct if pt in field_update]
                    ct = new_ct

                pti[field_name] = ct
        return

    security.declarePublic('getThumbnailTag')
    def getThumbnailTag(self, instance, field_name, **kwargs):
        """Generate an html img tag like OFS.Image but use specific thumb url"""

        # Get field
        field = instance.getField(field_name)

        # Get image
        accessor = field.getAccessor(instance)
        img = accessor()

        # If img doesn't exist returns an empty tag
        if not img:
            return ''

        # Check image class
        if not isinstance(img, Image):
            raise ValueError, 'Scale can only be applied on Image'

        # Get scale size
        width = kwargs.get('width', img.width)
        height = kwargs.get('height', img.height)
        maximizeTo = kwargs.get('maximizeTo', 0)
        maxRatio = kwargs.get('maxRatio', 0)
        width, height = self._getScaleSize(img, width, height, maximizeTo, maxRatio)

        # Get resource information
        content_type = img.content_type
        mtool = getToolByName(self, 'mimetypes_registry')
        mimes = mtool.lookup(content_type)
        ext = str(mimes[0].extensions[0])

        # Get some attributes
        title = kwargs.get('title', instance.title_or_id())
        alt = kwargs.get('alt', title)

        # Get tag url
        tag_url = instance.absolute_url()

        if HAS_PIL:
            tag_url += '/pa_thumb/%(field_name)sx%(width)sx%(height)s.%(ext)s' % {
                'field_name': field_name,
                'width': width,
                'height': height,
                'ext': ext,
                }

        values = {'src' : tag_url,
                  'alt' : escape(alt, 1),
                  'title' : escape(title, 1),
                  'height' : height,
                  'width' : width,
                 }

        result = '<img src="%(src)s" alt="%(alt)s" title="%(title)s" '\
                 'height="%(height)s" width="%(width)s"' % values

        for key, value in kwargs.items():
            if key not in ('width', 'height', 'title', 'alt',) and value:
                result = '%s %s="%s"' % (result, key, value)

        return '%s />' % result

    security.declarePublic('getThumbnail')
    def getThumbnail(self, instance, thumbnail_id, request=None):
        """Create scale of image

        @param instance: Content with ImageField
        @param thumbnail_id: <field_name>x<width>x<height>.<ext>"""

        if request is None:
            request = self.REQUEST
        response = request.RESPONSE

        # Parse thumbnail_id
        match = THUMBNAIL_RE.match(thumbnail_id)
        if match is None:
            raise ValueError, "Thumbnail id is bad formated"

        field_name = match.group('field_name')
        width = int(match.group('width'))
        height = int(match.group('height'))

        # Get image and scale it
        field = instance.getField(field_name)
        accessor = field.getAccessor(instance)
        img = accessor()

        return self.scaleImage(img, width, height).index_html(request, response)

    security.declarePublic('scaleImage')
    def scaleImage(self, img, width, height):
        """Return a scaled OFS.Image instance

        @param img: an OFS.Image instance.
        @param width: width in pixels
        @param height: height in pixels

        if img is not an Image, it is returned as is.
        """

        if type(img) in (StringType,) and len(img) == 0:
            return ''

        # Check image
        if not isinstance(img, Image):
            raise ValueError, 'Scale can only be applied on Image'

        if not HAS_PIL:
            return img

        # empty string - stop rescaling because PIL fails on an empty string
        if img.get_size() == 0:
            return ''

        # If null size returns empty string
        if width == 0 or height == 0:
            return ''

        size = int(width), int(height)
        image = PIL.Image.open(StringIO(img.data))
        # consider image mode when scaling
        # source images can be mode '1','L,','P','RGB(A)'
        # convert to greyscale or RGBA before scaling
        # preserve palletted mode (but not pallette)
        # for palletted-only image formats, e.g. GIF
        # PNG compression is OK for RGBA thumbnails
        original_mode = image.mode
        if original_mode == '1':
            image = image.convert('L')
        elif original_mode == 'P':
            image = image.convert('RGBA')
        image.thumbnail(size, PIL.Image.ANTIALIAS)
        # XXX: tweak to make the unit test
        #      test_fields.ProcessingTest.test_processing_fieldset run
        format = image.format and image.format or 'GIF'
        # decided to only preserve palletted mode
        # for GIF, could also use image.format in ('GIF','PNG')
        if original_mode == 'P' and format == 'GIF':
            image = image.convert('P')
        thumbnail_file = StringIO()
        # quality parameter doesn't affect lossless formats
        image.save(thumbnail_file, format, quality=88)
        thumbnail_file.seek(0)
        return Image('thumb', 'thumb', thumbnail_file, content_type='image/png')

    def _getScaleSize(self, img, width, height, maximizeTo=0, maxRatio=0):
        """Returns tuple(width, height) of scale
           if maximizeTo!=0 can return bigger dimensions than original
           if maxRatio=1 ratio is based on biggest width or height"""

        img_width = img.width
        img_height = img.height

        if img_width=="" or img_height=="":
            # img width and height not initiated
            return (0,0)

        width_ratio = 1.0
        height_ratio = 1.0
        if maximizeTo  :
           # ratio independant from original width, height
           width_ratio = float(maximizeTo)/img_width
           height_ratio = float(maximizeTo)/img_height
        else:
            # Get standard ratio
            if width is not None and width < img_width:
                width_ratio = float(width)/img_width
            if height is not None and height < img_height:
                height_ratio = float(height)/img_height
        if maxRatio :
            ratio = max(width_ratio, height_ratio)
        else:
            ratio = min(width_ratio, height_ratio)

        # Returned the scale size
        return int(ratio*img_width), int(ratio*img_height)

    security.declareProtected(CCP.ManagePortal, 'migrate')
    def migrate(self, **options):
        """
            Migrate articles
            See migrator documentation for options.
        """
        from Products.PloneArticle.migration import migrator
        return migrator.migrate(self, **options)

    security.declarePublic('cleanFilename')
    def cleanFilename(self, filename=''):
        """
        IE uploads file with full paths. This method return the single filename.
        """
        assert isinstance(filename, basestring)
        filename = os.path.basename(filename)
        return filename.split("\\")[-1]

    security.declarePublic('fileFromUpload')
    def fileFromUpload(self, id, title, uploaded_file, article):
        #f = File(id, title, uploaded_file)
        f = BaseUnit(id, uploaded_file, article)
        f.title = title # OFS File property
        return f

    security.declarePublic('getContentTypeOf')
    def getContentTypeOf(self, file_object, context):
        """
        return getContentType of file

        @param file_object: a File instance (or BaseUnit)

        @param context: the acquisition context to set on file. Required for
        security checks
        """
        return file_object.__of__(context).getContentType()

    security.declarePublic('imageFromUpload')
    def imageFromUpload(self, id, title, image_file):
        image = Image(id, title, image_file)
        return image

    security.declarePublic('getImageDimensions')
    def getImageDimensions(self, image):
        """
        Return width/height from an Image instance.
        The width and height are guaranteed to be integers.
        In case width and height can't be recovered, something
        must have gone wrong, and 0 is returned.
        This method is helpful for unprivileged scripts
        """
        width=0
        height=0
        # Try fetching width and height as int. If it fails, fall-back to 0.
        try:
            width=int(image.width)
        except:
            pass
        try:
            height=int(image.height)
        except:
            pass
        return width, height

    security.declarePublic('useAttachmentField')
    def useAttachmentField(self):
        """Returns True if AttachmentField product is installed"""

        return USE_ATTACHMENT_FIELD

    ### Version management

    security.declareProtected(CCP.ManagePortal, 'getVersion')
    def getVersion(self):
        """Get internal numversion and version
        """
        return self._numversion, self._version

    security.declareProtected(CCP.ManagePortal, 'getVersionFromFS')
    def getVersionFromFS(self):
        """Get numversion and version from FS
        """
        from Products.PloneArticle import __pkginfo__ as pkginfo
        return pkginfo.numversion, pkginfo.version.lower()

    security.declareProtected(CCP.View, 'needsVersionMigration')
    def needsVersionMigration(self):
        """Version migration is required when fs version != installed version
        """
        nv, v = self.getVersion()
        fsnv, fsv = self.getVersionFromFS()
        return nv != fsnv # or v != fsv ## fail for CVS/SVN

    security.declareProtected(CCP.ManagePortal, 'setInstanceVersion')
    def setInstanceVersion(self, version):
        """ The version this instance of plonearticle is on """
        self._version = version
        major, minor, suffix =  version.split('.')
        suffix = suffix.split('-')
        bugfix = suffix[0]
        release = len(suffix) > 1 and suffix[1] or ''
        self._numversion = (int(major), int(minor), int(bugfix), release)

    security.declareProtected(CCP.ManagePortal, 'setVersionFromFS')
    def setVersionFromFS(self):
        """Updates internal numversion and version from FS
        """
        self._numversion, self._version = self.getVersionFromFS()


    # add an exclamation in ZMI if migration needed
    def om_icons(self):
        icons = ({
                    'path':'misc_/PloneArticle/tool.gif',
                    'alt':self.meta_type,
                    'title':self.meta_type,
                 },)
        if self.needsVersionMigration():
            icons = icons + ({
                     'path':'misc_/PageTemplates/exclamation.gif',
                     'alt':'Error',
                     'title':'PloneArticle needs updating'
                  },)

        return icons

    # migration stuff
    security.declareProtected(CCP.ManagePortal, 'knownVersions')
    def knownVersions(self):
        """ All known version ids, except current one """
        versions = _upgradePaths.keys()
        versions.sort()
        return versions

    def _upgrade(self, version):
        version = version.lower()
        if not _upgradePaths.has_key(version):
            return None, ("Migration completed at version %s" % version,)

        newversion, function = _upgradePaths[version]
        res = function(self.aq_parent)
        return newversion, res

    security.declareProtected(CCP.ManagePortal, 'upgrade')
    def upgrade(self, REQUEST=None, dry_run=None, swallow_errors=True,
                force_instance_version=None):

        result_log = []
        instance_version = force_instance_version or self.getVersion()[1]

        if dry_run:
            result_log.append(("Dry run selected.", logging.INFO))

        # either get the forced upgrade instance or the current instance
        newv = getattr(REQUEST, "force_instance_version", instance_version)

        result_log.append(("Starting the migration from "
                    "version: %s" % newv, logging.INFO))

        while newv is not None:
            result_log.append(
                ("Attempting to upgrade from: %s" % newv, logging.INFO))
            try:
                newv, msgs = self._upgrade(newv)
                if msgs:
                    for msg in msgs:
                        # if string make list
                        if isinstance(msg, basestring):
                            msg = [msg,]
                        # if no status, add one
                        if len(msg) == 1:
                            msg.append(logging.INFO)
                        result_log.append(msg)
                if newv is not None:
                    result_log.append(("Upgrade to: %s, completed" % newv, logging.INFO))
                    self.setInstanceVersion(newv)

            except ConflictError:
                raise
            except:
                exc_type, exc_value, exc_tb = sys.exc_info()
                result_log.append(("Upgrade aborted", logging.ERROR))
                result_log.append(("Error type: %s" % exc_type, logging.ERROR))
                result_log.append(("Error value: %s" % exc_value, logging.ERROR))
                for line in traceback.format_tb(exc_tb):
                    result_log.append((line, logging.ERROR))

                # set newv to None
                # to break the loop
                newv = None
                if not swallow_errors:
                    for msg, sev in result_log: LOG.log(sev, msg)
                    raise
                else:
                    # abort transaction to safe the zodb
                    transaction.abort()

        result_log.append(("End of upgrade path, migration has finished", logging.INFO))

        if self.needsVersionMigration():
            result_log.append((("The upgrade path did NOT reach "
                        "current version"), logging.ERROR))
            result_log.append(("Migration has failed", logging.ERROR))
        else:
            result_log.append((
                "Your PloneArticle instance is now up-to-date.", logging.INFO))

        if dry_run:
            result_log.append(("Dry run selected, transaction aborted",
                               logging.INFO))
            transaction.abort()

        # log all this
        for msg, sev in result_log:
            LOG.log(sev, msg)

        return result_log

    ###
    ## Configlet helpers
    ###

    security.declareProtected(CCP.ManagePortal, 'configletThumbnails')
    def configletThumbnails(self, REQUEST=None):
        """Provides a structure for configlet thumbnails as
        [{'label': xxx, 'url': xxx, 'cssclass': xxx}, ...]
        """

        if REQUEST is None:
            REQUEST = self.REQUEST

        out = []
        tab_defs = (
            # (translated title, template id),
            (ArticleMessageFactory(u'label_article_preferences',
                                   default=u'PloneArticle Preferences'),
             'pa_management_form'),
            (PloneMessageFactory(u'models', default=u'Models')
             , 'pa_manage_models_form'),
            (PloneMessageFactory(u'images', default=u'Images'),
             'pa_manage_images_form'),
            (PloneMessageFactory(u'files', default=u'Attachments'),
             'pa_manage_attachments_form'),
            (PloneMessageFactory(u'links', default=u'Links'),
             'pa_manage_links_form')
            )

        for message, template_id in tab_defs:
            thumbnail = {
                'label': message,
                'url': self.absolute_url() + '/' + template_id,
                'css_class': None
                }
            if REQUEST.URL.endswith(template_id):
                thumbnail['css_class'] = "selected"
            out.append(thumbnail)
        return out


    security.declarePublic('isArticle')
    def isArticle(self, obj):
        """
        Return True if obj is an Article
        Used by portal_javascript/portal_css ...
        """
        if IPloneArticle.providedBy(obj) :
            return True


    security.declarePublic('isEditableArticle')
    def isEditableArticle(self, obj):
        """
        Return True if obj is an Article
        and user has permission to modify it.
        Used by portal_javascript/portal_css ...
        """
        if self.isArticle(obj):
            mtool = getToolByName(self, 'portal_membership')
            if mtool.checkPermission('Modify portal content', obj) :
                return True
                

    security.declarePublic('isEditableArticle')
    def useJquery(self, obj):
        """
        Return True if we're in an article
        and version of plone < 3.1
        """
        pmig = getToolByName(self, 'portal_migration')
        if IPloneArticle.providedBy(obj) and \
           pmig.getFSVersionTuple() < (3, 1) :    
            return True          


InitializeClass(PloneArticleTool)
registerToolInterface(PLONEARTICLE_TOOL, IPloneArticleTool)
