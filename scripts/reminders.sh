#!/bin/bash

# make this runnable
# chmod +x reminders.sh
# run every hour
# add to crontab -e
# # Every hour
# 0 * * * * /home/airith/public_html/perfectarch.antyc.ca/PerfectArchOrthotics/scripts/reminders.sh

# find all Reminders

file=`realpath ${BASH_SOURCE[0]}`
proj_dir=`dirname $(dirname $file)`

activate="$proj_dir/activate.sh"
venv=$(python -c 'import sys; print ("1" if hasattr(sys, "real_prefix") else "0")')
if [[ "$venv" == "0" ]]; then
    source "$activate"
fi

manage="$proj_dir/manage.py"
python $manage reminders

if [[ "$venv" == "0" ]]; then
    deactivate
fi
