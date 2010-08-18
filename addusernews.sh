#!/bin/sh
# leafnode preinstall script

name=news
uid=109
gid=109
nicl=/usr/bin/niutil

# test if user or group exist, if not: create them

$nicl -read . /users/$name >/dev/null 2>&1
if [ $? != 0 ] ;
then
	$nicl -create . /users/$name
	$nicl -createprop . /users/$name uid $uid
	$nicl -createprop . /users/$name gid $gid
	$nicl -createprop . /users/$name passwd '*'
	$nicl -createprop . /users/$name change 0
	$nicl -createprop . /users/$name expire 0
	$nicl -createprop . /users/$name realname 'NNTP Service'
	$nicl -createprop . /users/$name home '/var/spool/news'
	$nicl -createprop . /users/$name shell '/usr/bin/false'
	$nicl -createprop . /users/$name _writers_passwd $name
	echo "OK: User 'news' created."
else echo "Warning: User 'news' ($uid) already exists."
fi

$nicl -read . /groups/$name >/dev/null 2>&1
if [ $? != 0 ] ;
then
	$nicl -create . /groups/$name
	$nicl -createprop . /groups/$name gid $gid
	$nicl -createprop . /groups/$name passwd '*'
	echo "OK: Group 'news' created."
else echo "Warning: Group 'news' ($gid) already exists."
fi