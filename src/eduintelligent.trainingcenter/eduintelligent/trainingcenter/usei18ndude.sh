#!/bin/bash 

DOMAIN="eduintelligent.trainingcenter"
DOMAIN_PLONE="plone"
I18NDUDE=../../../../bin/i18ndude
# If you want to add another language create folders and empty file:
#   mkdir -p locales/<lang_code>/LC_MESSAGES
#   touch locales/<lang_code>/LC_MESSAGES/$DOMAIN.po
# and run this script
# Example:
#          mkdir -p locales/es/LC_MESSAGES
#          touch locales/es/LC_MESSAGES/iservces.theme.po

#More examples
# mkdir -p locales/{en,es}/LC_MESSAGES
# touch locales/{en,es}/LC_MESSAGES/$DOMAIN.po

echo "Syncing all translations for domain ${DOMAIN}."
touch locales/$DOMAIN.pot
$I18NDUDE rebuild-pot --pot locales/$DOMAIN.pot --create $DOMAIN ./
$I18NDUDE rebuild-pot --pot locales/$DOMAIN-$DOMAIN_PLONE.pot --create $DOMAIN_PLONE ./

# sync all locales
echo "Sync and Compile po files for domain ${DOMAIN} in locales dir"
# Compile po files
for lang in $(find locales -mindepth 1 -maxdepth 1 -type d); do
    if test -d $lang/LC_MESSAGES; then
        $I18NDUDE sync --pot locales/${DOMAIN}.pot $lang/LC_MESSAGES/${DOMAIN}.po
        msgfmt -o $lang/LC_MESSAGES/${DOMAIN}.mo $lang/LC_MESSAGES/${DOMAIN}.po
    fi
done

echo "Syncing all translations for domain plone."

touch i18n/${DOMAIN}-${DOMAIN_PLONE}.pot
$I18NDUDE rebuild-pot --pot i18n/${DOMAIN}-${DOMAIN_PLONE}.pot --create ${DOMAIN_PLONE} profiles/ dashboard/
#For Spanish
$I18NDUDE sync --pot i18n/${DOMAIN}-${DOMAIN_PLONE}.pot i18n/${DOMAIN}-${DOMAIN_PLONE}-es.po
