# Backup database/media to a json file, tar/gzip the json file

filename="default"
now=$(date +"%Y_%m_%d")

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

python3 manage.py dumpdata > "$idx".json
tar -czf ../backups/"$idx".tar.gz "$idx".json
tar -czf ../backups/media_"$idx".tar.gz "media/"
rm "$idx".json
