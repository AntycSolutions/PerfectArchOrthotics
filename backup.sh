#!/bin/bash

# Backup database/media
#  tar/gzip the json file and media folder
#  tar -xzf <file> to un-tar/gzip

filename="default"

now=$(date +"%Y_%m_%d")  # year_month_day

# cd into directory of this file
dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd $dir

# use settings decision file to name backup
if [ -e "../devl" ]; then
    filename="devl"
elif [ -e "../test" ]; then
    filename="test"
elif [ -e "../prod" ]; then
    filename="prod"
else
    echo 'settings decision file not found'
    exit 1
fi

idx="$filename"_"$now"

venv='../venv_perfect_arch'
# check if we need to activate the virtual environment
if [ -d "$venv" ]; then
    source activate.sh
fi

# exclude contenttypes as they are created during migrate
python3 manage.py dumpdata -e contenttypes > "$idx".json

# deactivate the virtual environment
if [ -d "$venv" ]; then
    deactivate
fi

tar -czf ../backups/"$idx".tar.gz "$idx".json
# Media folder is big, so overwrite it
tar -czf ../backups/media_"$filename".tar.gz "media/"

rm "$idx".json
