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
    emacs --batch \
	--eval "(add-to-list 'load-path \"$HOME/.emacs.d/org-mode/lisp/\")" \
	--load=$HOME/.emacs.d/org-mode/lisp/org.el \
	--visit=MyFile --funcall org-export-as-html-batch
fi

help() {
    echo "pass a file to export"
}
