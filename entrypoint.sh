#!/bin/bash

# Save current env to crontab_env and crontab job can access docker env
CRONTAB_ENV=/crontab_env
printenv | sed 's/^\(.*\)$/export \1/g' > $CRONTAB_ENV

/usr/sbin/crond -n
