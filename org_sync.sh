#!/usr/bin/env bash

DEST=$HOME/Dropbox/org-copy

mkdir -p $DEST
rsync -avz $HOME/org/*.org $DEST/
