python ./manage.py wait_pg
python ./manage.py migrate
# python ./manage.py import_data
python ./manage.py search_index --rebuild --parallel
apt install -y curl
# python ./manage.py runserver
gunicorn movies.wsgi:application --bind 0.0.0.0:8000