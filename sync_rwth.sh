#!/bin/bash
# sinchronize pdf files in the rwth account
# Useful when you need to print something out

rsync -avz --delete-after --prune-empty-dirs --include '*/' --include '*.pdf' --exclude '*' $HOME/uni/aachen/ $HOME/Documents/trips/sardegna rwth:pdfs