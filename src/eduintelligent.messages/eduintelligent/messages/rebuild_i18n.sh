#!/bin/sh
PRODUCTNAME=eduintelligent.messages
I18NDOMAIN=$PRODUCTNAME
I18NDUDE=/Users/erik/Desarrollo/demo1/bin/i18ndude
# Synchronise the .pot with the templates.
# Also merge it with generated.pot, which includes the items
# from schema.py
$I18NDUDE rebuild-pot --pot locales/${PRODUCTNAME}.pot --create ${I18NDOMAIN} browser/

# Synchronise the resulting .pot with the .po files
$I18NDUDE sync --pot locales/${PRODUCTNAME}.pot locales/es/LC_MESSAGES/${PRODUCTNAME}-es.mo locales/es/LC_MESSAGES/${I18NDOMAIN}-es.po

# Zope3 is lazy so we have to comile the po files ourselves
msgfmt -o locales/es/LC_MESSAGES/${PRODUCTNAME}-es.mo locales/es/LC_MESSAGES/${I18NDOMAIN}-es.po
#msgfmt -o locales/es/LC_MESSAGES/${PRODUCTNAME}-plone-es.mo locales/es/LC_MESSAGES/${I18NDOMAIN}-plone-es.po
