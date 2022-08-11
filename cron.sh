#!/bin/sh

# start cron
env >> /etc/environment
cron -f -l 8