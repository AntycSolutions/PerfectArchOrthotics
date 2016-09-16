#!/bin/bash

# Backup database/media
#  tar/gzip the json file and media folder
#  tar -xzf <file> to un-tar/gzip

filename="default"
now=$(date +"%Y_%m_%d")
dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd $dir

if [ -e "../devl" ]
then
    filename="devl"
elif [ -e "../test" ]
then
    filename="test"
elif [ -e "../prod" ]
then
    filename="prod"
fi

idx="$filename"_"$now"

# exclude contenttypes as they are created during migrate
python3 manage.py dumpdata -e contenttypes > "$idx".json
tar -czf ../backups/"$idx".tar.gz "$idx".json
# Media folder is big, so overwrite it
tar -czf ../backups/media_"$filename".tar.gz "media/"
rm "$idx".json
