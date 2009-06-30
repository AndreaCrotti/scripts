#!/bin/bash

# Pass as input the file you want to convert to html

FILE=$1

ORG=/usr/share/emacs/site-lisp/org.el

if ! test -f $FILE
then
    echo "file not present"
else
    echo "converting file $FILE"
    # TODO putting a minimal init file
    emacs --no-init-file --batch --load=$ORG --visit=$FILE --eval "(setq org-export-headline-levels 2)" --funcall (org-export-as-html-batch)
fi