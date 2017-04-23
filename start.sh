#!/bin/sh
nohup uwsgi /home/liaotian-robot/config.ini > uwsgi.log 2>&1 &
