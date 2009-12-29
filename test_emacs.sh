#!/bin/bash
set -x
CONF="$HOME/.emacs.d/init.el"
EMACS="/Applications/Emacs.app/Contents/MacOS/Emacs"
#EMACS="emacs"
# TODO: set the conf to the argument passed otherwise    
$EMACS --batch --eval "(condition-case err (progn (load \"$CONF\"))) (kill-emacs 0)) (error (kill-emacs 1)))"
