#!/bin/bash
locale -a
export FLASK_APP=app.py 
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

/usr/bin/python3 ./init.py
/usr/bin/python3 -m flask run --host=0.0.0.0
