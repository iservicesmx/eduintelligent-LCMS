#!/bin/bash 

DOMAIN="eduintelligent.courses"
DOMAIN_PLONE="plone"
I18NDUDE=../../../../bin/i18ndude
# If you want to add another language create folders and empty file:
#   mkdir -p locales/<lang_code>/LC_MESSAGES
#   touch locales/<lang_code>/LC_MESSAGES/$DOMAIN.po
# and run this script
# Example: locales/hu/LC_MESSAGES/$DOMAIN.po

touch locales/$DOMAIN.pot
$I18NDUDE rebuild-pot --pot locales/$DOMAIN.pot --create $DOMAIN ./
$I18NDUDE rebuild-pot --pot locales/$DOMAIN-$DOMAIN_PLONE.pot --create $DOMAIN_PLONE ./

# sync all locales
find locales -depth -type d   \
     | grep -v .svn \
     | grep -v LC_MESSAGES \
     | sed -e "s/locales\/\(.*\)$/\1/" \
     | xargs -I % $I18NDUDE sync --pot locales/$DOMAIN.pot locales/%/LC_MESSAGES/$DOMAIN.po

# sync all locales
find locales -depth -type d   \
     | grep -v .svn \
     | grep -v LC_MESSAGES \
     | sed -e "s/locales\/\(.*\)$/\1/" \
     | xargs -I % $I18NDUDE sync --pot locales/$DOMAIN-$DOMAIN_PLONE.pot locales/%/LC_MESSAGES/$DOMAIN-$DOMAIN_PLONE.po
     
     
