#!/bin/bash

ORG="$HOME/.emacs.d/org-mode/lisp/"
EMACS="/Applications/Emacs.app/Contents/MacOS/Emacs"

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
    $EMACS   --batch \
	--eval "(add-to-list 'load-path \"$ORG\")" \
	--eval "(require 'org)" \
	--visit=$FILE --funcall org-export-as-latex-batch
fi

