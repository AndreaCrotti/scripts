#!/bin/bash

ORG="$HOME/.emacs.d/org-mode/lisp/"
EMACS="/Applications/Emacs.app/Contents/MacOS/Emacs"
PREAMBLE="(add-to-list 'load-path \"$ORG\")(require 'org)"

usage () {
    echo "org_html.sh <org_file>"
    exit 1
}

if test $# -lt 2
then
    usage
fi

# using getopt or getopts to get the arguments
FILE=$1

if ! test -f $FILE
then
    help
else
    echo "converting file $FILE"
    $EMACS --batch \
	--eval $PREAMBLE
	--visit=$FILE --funcall org-export-as-latex-batch
fi

function export_calendar () {
    $EMACS --batch \
	--eval \
	"(progn (load-file \"~/elisp/org/org.el\") \
        (load-file \"~/elisp/org/org-install.el\") \
        (load-file \"~/elisp/org-batch-config.el\") \
        (setq org-icalendar-combined-name \"Your Calendar\") \
        (setq org-combined-agenda-icalendar-file \"~/org/cal/your-calendar.ics\") \
        (setq org-agenda-files (quote (\"~/org/cal/your-calendar.org\"))))" \
}
