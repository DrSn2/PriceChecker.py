#!/bin/bash
Xvfb :0 -screen 0 1024x768x24 >/dev/null 2>&1 &
export DISPLAY=:0
env python runserver.py
