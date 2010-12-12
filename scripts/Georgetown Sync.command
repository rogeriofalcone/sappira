# replace the first line below with the path to your own django project
cd /users/brendanlevy/dropbox/sites/sappira/
rm georgetown.db
python manage.py syncdb --noinput
python manage.py runserver