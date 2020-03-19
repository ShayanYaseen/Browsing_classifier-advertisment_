curr_path=$PWD
history_script="/DMS/"
history_script="$curr_path$history_script"
web_app="/web-app/dashboard/"
web_app="$curr_path$web_app"

pushd $history_script
python3 history_display.py
popd
pushd $web_app
python3 manage.py runserver
