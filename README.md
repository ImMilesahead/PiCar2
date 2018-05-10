# PiCar2

##### About #####

This program is designed to be ran on a raspberry pi 3 attached to a 800x480 touch screen mounted where a car stereo would normally be.
It also (should) have functionality to utilize a OBD2 sensor in modern vehicles.


##### Installation instructions #####

[code]
$ cd
$ git clone https://github.com/ImMilesAhead/PiCar2.git
[/code]

Boom! Done! Installed!
Won't run though. The way it is designed is for there to be a directory in /home/$USER/PiCar2/ called Media. In this folder there will need to be a couple subfolders being Music, Pictures, Videos, and Playlists. we'll create those now 

##### Setup instructions #####

[code]
$ cd PiCar2
$ mkdir Media
$ mkdir Media/Music
$ mkdir Media/Pictures
$ mkdir Media/Videos
$ mkdir Media/Playlists 
[/code]

[code] Media/Music [/code] is where we'll dumb all of the songs. These will be sorted through and ategorized by mutagen based on metadata tags such as song name, song artist, and album

###### Dependecies ######

Libraries used are 
Mutagen, os, sys, platform, pygame, datetime, and random

The only libraries that should need to be installed are mutagen and pygame.

In the future I plan to add functionality that uses dlib face_recognition and pyobd2, but I'll include those here when the time comes.

to run simply 
[code] $ python Main.py [/code]
assuming python is installed and you are in the PiCar directory