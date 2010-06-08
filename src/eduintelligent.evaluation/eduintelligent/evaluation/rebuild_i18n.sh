#!/bin/sh
PRODUCTNAME=eduintelligent.evaluation
I18NDOMAIN=$PRODUCTNAME
I18NDUDE=../../../../bin/i18ndude
# Synchronise the .pot with the templates.
# Also merge it with generated.pot, which includes the items
# from schema.py
$I18NDUDE rebuild-pot --pot locales/${PRODUCTNAME}.pot --create ${I18NDOMAIN} ./

# Synchronise the resulting .pot with the .po files
$I18NDUDE sync --pot locales/${PRODUCTNAME}.pot locales/en/LC_MESSAGES/${I18NDOMAIN}.po

$I18NDUDE sync --pot locales/${PRODUCTNAME}.pot locales/es/LC_MESSAGES/${I18NDOMAIN}.po

# Zope3 is lazy so we have to comile the po files ourselves
#msgfmt -o locales/es/LC_MESSAGES/${PRODUCTNAME}-es.mo locales/es/LC_MESSAGES/${I18NDOMAIN}-es.po
#msgfmt -o locales/es/LC_MESSAGES/${PRODUCTNAME}-plone-es.mo locales/es/LC_MESSAGES/${I18NDOMAIN}-plone-es.po
