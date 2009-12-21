#!/bin/bash

# Pass as input the file you want to convert to html

FILE=$1
ORG="$HOME/.emacs.d/org-mode/lisp/org.el"

if ! test -f $FILE
then
    echo "file not found"
else
    echo "converting file $FILE"
    # # TODO putting a minimal init file
    # emacs --batch \
    # 	--eval "(add-to-list 'load-path \"$HOME/.emacs.d/org-mode/lisp/\")" \
    # 	--load=$HOME/.emacs.d/org-mode/lisp/org.elc \
    # 	orglib=$HOME/.emacs.d/org-mode/lisp/
    orglib=$HOME/.emacs.d/org-mode/lisp/
    emacs   --batch \
	--eval "(add-to-list 'load-path \"$HOME/.emacs.d/org-mode/lisp/\")" \
	--eval "(setq debug-on-error t)" \
	--eval "(require 'org)" \
	--eval "(require 'org-install)" \
	--visit=$FILE -f org-export-as-latex-batch
fi
	#--load=$orglib/org.el \

#orglib=$HOME/.emacs.d/org-mode/lisp/
# emacs   --batch \
#     --load=$orglib/org.elc \
#     --eval "(setq org-export-headline-levels 2)" \
#     --visit=$1 --funcall org-export-as-latex-batch

help() {
    echo "pass a file to export"
}
