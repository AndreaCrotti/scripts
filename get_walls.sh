#!/bin/bash
#NatGeo wallpapers script: This script downloads all the National Geographic wallpapers from the 2009 wallpaper contest
#the script will download more or less 170 wallpapers from the NatGeo webpage.
#I used the script from http://www.webupd8.org to get all the wallpapers:
#(http://www.webupd8.org/2009/11/automatically-download-all-wallpapers.html)
#Based on the cosmo wallpaper set of gnome 2.28
#All wallpapers are property of: Â© 2009 National Geographic Society
#The script is licensed GPLv3 by me, all doubts and proposals feel free to email to rafael.rojassegoviano<at>gmail.com

WALLS="$HOME/wallpapers"
if [ -d $WALLS ]
then
	echo "The wallpaper set is already installed!"
	exit 1
else
	mkdir $WALLS
	cd $WALLS

	for a in `jot - 1 26`
	do
	    wget "http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/1109wallpaper-"$a"_1600.jpg"
	    wget "http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/1102wallpaper-"$a"_1600.jpg"
	    wget "http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/1026wallpaper-"$a"_1600.jpg"
	    wget "http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/1019wallpaper-"$a"_1600.jpg"
	    wget "http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/1013wallpaper-"$a"_1600.jpg"
	    wget "http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/1005wallpaper-"$a"_1600.jpg"
	    wget "http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/0928wallpaper-"$a"_1600.jpg"
	    wget "http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/0921wallpaper-"$a"_1600.jpg"
	    wget "http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/0914wallpaper-"$a"_1600.jpg"
	    wget "http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/0907wallpaper-"$a"_1600.jpg"
	    wget "http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/0831wallpaper-"$a"_1600.jpg"
	    wget "http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/0824wallpaper-"$a"_1600.jpg"
	done
fi
