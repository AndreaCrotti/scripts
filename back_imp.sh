#!/bin/bash
IMP="$HOME/uni $HOME/Documents $HOME/Pictures $HOME/pycon $HOME/xype"
DEST=/media/usbhd-sdb1/back/
rsync -az --progress $IMP $BACK
