#!/bin/bash

i18ndude rebuild-pot --pot userandgroupselectionwidget.pot --create userandgroupselectionwidget --merge manual.pot `find ../skins/userandgroupselectionwidget -iregex '.*\..?pt$'`

i18ndude  sync --pot userandgroupselectionwidget.pot  `find . -iregex '.*\.po$'`

