#!/bin/bash

EMACS="emacs -Q"

usage () {
    echo "org_html.sh <org directory> <txt|pdf|html> <org files>"

    exit 1
}

if test $# -lt 3
then
    usage
fi

$ORG_DIR=$1
$FMT=$2
# $ORG_FILES=$3 # or use *.org as default maybe
PREAMBLE="(add-to-list 'load-path \"$ORG_DIR\")(require 'org)"

# using getopt or getopts to get the arguments
FILE=$3


if ! test -f $FILE
then
    usage
else
    echo "converting file $FILE"
    $EMACS --batch \
	--eval $PREAMBLE \
	--visit=$FILE --funcall org-export-as-html-batch
fi

# function export_calendar () {
#     $EMACS --batch \
# 	--eval \
# 	"(progn (load-file \"~/elisp/org/org.el\") \
#         (load-file \"~/elisp/org/org-install.el\") \
#         (load-file \"~/elisp/org-batch-config.el\") \
#         (setq org-icalendar-combined-name \"Your Calendar\") \
#         (setq org-combined-agenda-icalendar-file \"~/org/cal/your-calendar.ics\") \
#         (setq org-agenda-files (quote (\"~/org/cal/your-calendar.org\"))))" \
# }
