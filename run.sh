pip3 install csvtotable 
pip3 install plotly
curr_path=$PWD
history_script="DMS/"
web_app="web-app/dashboard/"
data="web-app/dashboard/static/data/"
pushd $history_script
python3 history_display.py
python3 ads_categorization.py
popd
pushd $data
csvtotable -o ad.csv ad_embed.html
csvtotable -o history.csv history_embed.html
csvtotable -o visit.csv visit_embed.html
rm ad.csv history.csv visit.csv
popd
pushd $web_app
python3 manage.py runserver

