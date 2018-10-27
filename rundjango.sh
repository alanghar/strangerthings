#!/bin/bash
#export DISPLAY=:0.0
#clear
#cd 
#cd /home/pi/playerhud-git/playerhud/djangogamemanager
cd /home/pi/src/strangerthings
source env/bin/activate
cd lights
sudo python ./manage.py runserver 0.0.0.0:80 &
#sleep 7
#gnome-terminal -e "sudo -H -u pi bash -c \"/usr/bin/chromium-browser  --start-fullscreen --start-maximized --disable-session-crashed-bubble http://localhost:8000/hintconsole/\"" 
