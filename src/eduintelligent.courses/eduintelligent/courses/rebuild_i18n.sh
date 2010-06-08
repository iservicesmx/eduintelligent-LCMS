#!/bin/sh
PRODUCTNAME=eduintelligent.courses
I18NDOMAIN=$PRODUCTNAME

# Synchronise the .pot with the templates.
# Also merge it with generated.pot, which includes the items
# from schema.py
#i18ndude rebuild-pot --pot i18n/${PRODUCTNAME}.pot --create ${I18NDOMAIN} browser/

# Synchronise the resulting .pot with the .po files
#i18ndude sync --pot i18n/generated.pot i18n/traincenter-es.po

# Zope3 is lazy so we have to comile the po files ourselves
msgfmt -o locales/es/LC_MESSAGES/eduintelligent.courses-es.mo locales/es/LC_MESSAGES/eduintelligent.courses-es.po
msgfmt -o locales/es/LC_MESSAGES/eduintelligent.courses-plone-es.mo locales/es/LC_MESSAGES/eduintelligent.courses-plone-es.po
