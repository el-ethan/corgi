
#!/bin/bash

KIVYPATH="/home/ethan/Dropbox/development/kivy_fork" 

export PYTHONPATH="$PYTHONPATH:$KIVYPATH/kivy"
export KIVY_HOME="$KIVYPATH/.kivy"

python ~/Dropbox/development/corgi/corgi.py $1
