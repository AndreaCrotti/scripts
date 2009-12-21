#!/bin/bash

PW=$(echo $1 | md5 | cut -c 1-7)
echo $PW
