#!/bin/sh
ps -ef|grep uwsgi|awk '{print $2}'|xargs -n1 kill -9
