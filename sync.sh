rm db.sqlite3
rm clients/migrations/0*
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
python3 populate.py
