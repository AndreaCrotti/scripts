#!/usr/bin/env bash

for cfg in $(sudo snapper --no-headers --csvout -c root list --columns number)
do
    echo "deleting $cfg"
    sudo snapper -c root delete $cfg;
done
