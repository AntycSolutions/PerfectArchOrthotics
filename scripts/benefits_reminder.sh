#!/bin/bash

# send benefits reminders to Clients

file=`realpath ${BASH_SOURCE[0]}`
proj_dir=`dirname $(dirname $file)`

activate="$proj_dir/activate.sh"
venv=$(python -c 'import sys; print ("1" if hasattr(sys, "real_prefix") else "0")')
if [[ "$venv" == "0" ]]; then
    source "$activate"
fi

manage="$proj_dir/manage.py"
python $manage benefits_reminder

if [[ "$venv" == "0" ]]; then
    deactivate
fi
