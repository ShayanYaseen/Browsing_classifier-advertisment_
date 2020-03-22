curr_path=$PWD
history_script="DMS/"
web_app="web-app/dashboard/"

pushd $history_script
python3 history_display.py
python3 ads_categorization.py
popd
pushd $web_app
python3 manage.py runserver
