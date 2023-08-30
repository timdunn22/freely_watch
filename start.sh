python ./manage.py wait_pg
python ./manage.py makemigrations
python ./manage.py migrate
# python ./manage.py all_processing
python ./manage.py search_index --rebuild --parallel
apt install -y curl --fix-missing
# python ./manage.py runserver
gunicorn movies.wsgi:application --bind 0.0.0.0:8000
# uvicorn ./fast_version/main:app --reload --port=4000