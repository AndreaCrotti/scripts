#!/bin/bash
OPTIOSN=$1
rsync -avz $OPTIOSN koalawlan::data $HOME
