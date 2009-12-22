#!/bin/bash

FILE=$1
ORG="$HOME/.emacs.d/org-mode/lisp/"
EMACS="/Applications/Emacs.app/Contents/MacOS/Emacs"

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

help() {
    echo "org_html.sh <org_file>"
    exit 1
}
