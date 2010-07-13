#!/bin/bash
virtualenv2.6 --no-site-packages $1
cd $1
source bin/activate
easy_install extremes
easy_install PasteScript
easy_install -i http://www.turbogears.org/2.0/downloads/current/index tg.devtools
