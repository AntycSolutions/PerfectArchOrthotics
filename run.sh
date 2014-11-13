[ "$1" == 'test' ] && ( python3 manage.py runserver 0.0.0.0:8080; exit 1 )

python3 manage.py runserver 127.0.0.1:8080
