#!/bin/bash

# Pass as input the file you want to convert to html

FILE=$1
ORG="$HOME/.emacs.d/org-mode/lisp/org.el"

if ! test -f $FILE
then
    echo "file not found"
else
    echo "converting file $FILE"
    # TODO putting a minimal init file
    emacs --no-init-file --batch --visit=$FILE --eval \
	"(progn
         (add-to-list 'load-path \"~/.emacs.d/org-mode/site-lisp/\")
         (require 'org)
         (require 'org-html)
         (require 'org-macs))" \
    -f org-export-as-html-batch
fi

help() {
    echo "pass a file to export"
}
