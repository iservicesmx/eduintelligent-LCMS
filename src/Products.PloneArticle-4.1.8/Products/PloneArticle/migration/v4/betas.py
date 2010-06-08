# Copyright (C) 2003-2006 Ingeniweb SAS

# This software is subject to the provisions of the GNU General Public
# License, Version 2.0 (GPL).  A copy of the GPL should accompany this
# distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY,
# AGAINST INFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE

# More details in the ``LICENSE`` file included in this package.

"""
    Plone Article migration module
"""

# Python imports
from StringIO import StringIO
from types import IntType
import sys
import itertools

import transaction

# Zope imports
from OFS.Image import File
from zExceptions import NotFound

# We need to run some methods with all permissions
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.User import UnrestrictedUser

# CMF imports
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.interfaces.base import IBaseUnit
from Products.CMFPlone.utils import safe_hasattr

from Products.PloneArticle.version import getArticleVersionFor
from Products.PloneArticle.migration import applyArticles
from Products.PloneArticle import LOG

def generateUniqueId(type_name=None):
    """
        Generate an id for the content
        This is not the archetype's uid.
    """
    from DateTime import DateTime
    from random import random

    now = DateTime()
    time = '%s.%s' % (now.strftime('%Y-%m-%d'), str(now.millis())[7:])
    rand = str(random())[2:6]
    prefix = ''
    suffix = ''

    if type_name is not None:
        prefix = type_name.replace(' ', '_') + '.'
    prefix = prefix.lower()

    return prefix + time + rand + suffix
def get322Contents(article, orderedListName, internal=True):
    """
        Return all the images that are linked in an article.

        article is a 3.x.x article
        orderedListName is the name of the attributes which contain the ordered
        list of contents.
             It can be either '__ordered_attachment_refs__', '__ordered_image_refs__'
             or '__ordered_link_refs__'.
        if internal is True, return Images detected as internal, else
        return images given in reference.
    """

    LOG.debug("migration.get322Contents parameters:\n %s %s %s" % (article.absolute_url(), orderedListName, repr(internal)))
    if not safe_hasattr(article, "at_references"):
        raise ValueError("Article has no at_references attribute.")

    result = []
    if internal:
        # During migration from old Plone and Zope versions some references
        # are inconsistant.
        # To be sure to migrate all inner content we **guess** that only one inner
        # type contains word in portal_type or in meta_type to filter out other
        # inner types.
        word = ''
        if orderedListName == '__ordered_attachment_refs__':
            word = 'file'
        elif orderedListName == '__ordered_image_refs__':
            word = 'image'
        elif orderedListName == '__ordered_link_refs__':
            word = 'link'
        else:
            # XXX Ouch, it's some unknown orderedListName: try and pray.
            word = 'file'

        result.extend([obj for obj in article.objectValues()
                       if word in obj.portal_type.lower() or word in obj.meta_type.lower()])
        LOG.debug("inner content for word %s:\n %s" % (word, repr(result)))

    try:
        oList = getattr(article, orderedListName)
    except AttributeError, e:
        # There's something bad there. As we don't want the migration fail here
        # we put a log in 'error' level.
        LOG.error("migration.get322Contents:\n%s attribute does'nt exist for %s" % (orderedListName, article.absolute_url()))
        return result

    for refUid in oList.getItems():
        ref = getattr(article.at_references, refUid)
        ## don't use hasattr (it uses aquisition) use safe_hasattr
        try:
            obj = ref.getTargetObject()
        except AttributeError, e: ## in some case, there is some ghost references...
            LOG.debug("Atributerror during migration on %s" % e)
            continue ## just ignore it...
        if safe_hasattr(article, obj.id) and internal:
            if obj not in result:
                result.append()
        elif not safe_hasattr(article, ref.getTargetObject().id) and not internal:
            result.append(ref.getTargetObject())

    return result


def migrateImages322to400(article, out):
    ## looking for old images
    intImages = get322Contents(article, "__ordered_image_refs__", internal=True)
    extImages = get322Contents(article, "__ordered_image_refs__", internal=False)

    ## article
    ##     images (ImageInnerContent)
    ##         ImageInnerContentProxies (as many as images)
    ##             attachedImage or
    ##             referencedContent
    ##             (image) -> just a computed field
    ##             title
    ##             description
    ##
    ##     links
    ##     files

    values = []
    for image in intImages:
        value = { ## this are the fields of ImageInnerContentProxy
            "attachedImage": (image.getImage(), {}),
            "title": (image.Title(), {}),
            "description": (image.Description(), {}),
            "id": (generateUniqueId("imageProxy"), {}),
        }
        values.append(value)
    for image in extImages:
        value = { ## this are the fields of ImageInnerContentProxy
            "referencedContent": (image, {}),
            "title": (image.Title(), {}),
            "description": (image.Description(), {}),
            "id": (generateUniqueId("imageProxy"), {}),
        }
        values.append(value)

    # XXX Something make us loose right, but we are pragmatic
    current_user = getSecurityManager().getUser()
    newSecurityManager(None, UnrestrictedUser('manager', '', ['Manager'], []))
    article.setImages(values)
    newSecurityManager(None, current_user)

def migrateFiles322to400(article, out):
    intFiles = get322Contents(article, "__ordered_attachment_refs__", internal=True)
    extFiles = get322Contents(article, "__ordered_attachment_refs__", internal=False)

    values = []
    for file in intFiles:
        value = { ## this are the fields of ImageInnerContentProxy
            "attachedFile": (file.getFile(), {}),
            "title": (file.Title(), {}),
            "description": (file.Description(), {}),
            "id": (generateUniqueId("fileProxy"), {}),
        }
        values.append(value)
    for file in extFiles:
        value = { ## this are the fields of ImageInnerContentProxy
            "referencedContent": (file, {}),
            "title": (file.Title(), {}),
            "description": (file.Description(), {}),
            "id": (generateUniqueId("fileProxy"), {}),
        }
        values.append(value)

    # XXX Something make us loose right, but we are pragmatic
    current_user = getSecurityManager().getUser()
    newSecurityManager(None, UnrestrictedUser('manager', '', ['Manager'], []))
    article.setFiles(values)
    newSecurityManager(None, current_user)

def migrateLinks322to400(article, out):
    intLinks = get322Contents(article, "__ordered_link_refs__", internal=True)
    extLinks = get322Contents(article, "__ordered_link_refs__", internal=False)

    values = []
    for link in intLinks:
        value = { ## this are the fields of ImageInnerContentProxy
            "attachedLink": (link.getRemoteUrl(), {}),
            "title": (link.Title(), {}),
            "description": (link.Description(), {}),
            "id": (generateUniqueId("linkProxy"), {}),
        }
        values.append(value)
    for link in extLinks:
        value = { ## this are the fields of ImageInnerContentProxy
            "referencedContent": (link, {}),
            "title": (link.Title(), {}),
            "description": (link.Description(), {}),
            "id": (generateUniqueId("linkProxy"), {}),
        }
        values.append(value)

    # XXX Something make us loose right, but we are pragmatic
    current_user = getSecurityManager().getUser()
    newSecurityManager(None, UnrestrictedUser('manager', '', ['Manager'], []))
    article.setLinks(values)
    newSecurityManager(None, current_user)


def migrateModel322to400(article, out):
    out.write("Models migration: ")
    if article.model in  ('pa_model', 'plonearticle_model'):
        newModel = "pa_model1"
    elif article.model.startswith('plonearticle_model'):
        ## We keep only the last number as known models are between 1 and 6
        newModel = 'pa_model' + article.model[-1]
    else:
        newModel = article.model
    article.setLayout(newModel)
    out.write("old model %s || new model %s\r\n" % (article.model, repr(article.getLayout())))

def clean322to400(article, out):

    ## Do not remove ids of objects like files or images, since
    ## when deleted, they do not apear anymore even if they are stored in
    ## the proxy.

    attributesToRemove = [
        "__ordered_attachment_refs__",
        "__ordered_image_refs__",
        "__ordered_link_refs__",
        "_locked_by",
        "_locked_date",
        "_objects",
        "_unlocked_by",
        "_unlocked_date",
        "model",
    ]
    for attr in attributesToRemove:
        try:
            delattr(article, attr)
        except AttributeError:
            pass


def migrateArticle322to400(article, out):

    out.write("Migrating article at '%s'\r\n" % article.absolute_url())

    migrateImages322to400(article, out)
    migrateFiles322to400(article, out)
    migrateLinks322to400(article, out)

    migrateModel322to400(article, out)

    clean322to400(article, out)
    out.write("success!\r\n\r\n")

def migrateArticle(article, out):
    migrateArticle322to400(article, out)

def migrateArticles(portal, article_brains, out):
    """
        Migrate all PloneArticle 3.x to PloneArticle 4.0.0
        article_brains is a collection of brains of article
    """

    plonearticle_tool = getToolByName(portal, 'plonearticle_tool')

    out.write('Migrate PloneArticle v3.x to v4.0.0.\r\n')

    nb_articles = 0
    already = 0

    out.write("There are %d PloneArticle objects.\r\n\r\n" % len(article_brains))

    # Get all PloneArticle in v3.x
    for article_brain in article_brains:
        try:
            article = article_brain.getObject()

            # Check if it has not been done before
            if article.getPAVersion() ==  (4, 0, '0-beta4'):
                already += 1
                continue

            # This is an article from v3.x
            parent = article.getParentNode()
            nb_articles += 1
            migrateArticle(article, out)
        except NotFound, e:
            out.write("%s not found.\r\n" % e)

    left = len(article_brains) - already - nb_articles
    out.write('%s article(s) migrated.\r\n' % nb_articles)
    out.write('%s article(s) were already migrated.\r\n' % already)
    out.write('%s article(s) left unmigrated.\r\n' % left)
    if left > 0:
        out.write('Please launch migration process again.\r\n')
    else:
        out.write('\n')
    out.write('Migration from PloneArticle v3.x to v4.0.0 finished.\r\n')

def v3_v4beta1(portal):
    """Migrate from v3.x to v4.0.0beta1    """

    out = StringIO()
    portal_catalog = getToolByName(portal, 'portal_catalog')
    article_brains = portal_catalog(portal_type='PloneArticle')
    migrateArticles(portal, article_brains, out)
    return (out.getvalue(),)

###############################################################################

def beta3_beta4(portal):
    """4.0.0beta3 to beta4"""
    out = []

    version = getArticleVersionFor('4.0.0-beta4')

    def modifyArticle(article):
        # fix version. Earlier v4 articles don't have one
        # post beta4 should have an integer number (value >= 0)
        if type(article.getPAVersion()) is not IntType:
            article.setPAVersion(version)

        # rename proxy if necessary
        file_proxies = tuple(article.getFiles()) + tuple(article.getImages())
        for proxy in file_proxies:
            proxy.renameFromFileName()

    applyArticles(portal, modifyArticle)

    out.append("Set version information on older articles")
    out.append("Renamed proxy files and images ids to stored filename")
    return out


###############################################################################

def beta5_beta6(portal):
    """4.0.0beta5 to beta6"""
    out = []

    def modifyModel(article):
        # fix model. Earlier beta6 articles model migration is broken
        model = article.layout
        if model is None:
            article.setLayout('pa_model1')
        elif model.startswith('pa_odel'):
            article.setLayout('pa_model' + model[-1])

    applyArticles(portal, modifyModel)
    out.append("Fix model migration on older articles")

    if 'portal_article' in portal.objectIds():
        portal.manage_delObjects(['portal_article',])
        out.append("Delete old article tool")

    return out
