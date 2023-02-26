from flask import Flask
from flask import render_template, request
from flask_wtf.csrf import CSRFProtect
from geopy.geocoders import Nominatim
import psutil
import requests


app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app)
geolocator = Nominatim(user_agent="pyp-boy")

## def general vars for footer
def footer_vars():
    cpu_percent = psutil.cpu_percent(interval=0.1)
    footer_vars = {
        'cpu_percent': cpu_percent,
    }

    return footer_vars

footer_vars = footer_vars()

@app.route("/")
@app.route("/stat")
def stat():
    return render_template('stat.html', footer_vars=footer_vars)

@app.route("/inv")
def inventory():
    return render_template('inv.html', footer_vars=footer_vars)

@app.route("/map", methods=['GET'])
@app.route("/map/", methods=['GET'])
def map():
    url = 'https://ipinfo.io/json'
    response = requests.get(url)
    get_latitude = request.args.get('latitude', '0')
    get_longitude = request.args.get('longitude', '0')

    if get_latitude == '0' and get_longitude == '0':
        geoloc_request = response.json()['loc']
    else:
        geoloc_request = str(get_latitude) + ',' +str(get_longitude)

    print(geoloc_request)
    location = geolocator.geocode(geoloc_request)
    return render_template('map.html', footer_vars=footer_vars, location=location)

@app.route("/map/search", methods=('GET', 'POST'))
def map_search():
    if request.method == 'POST':
        map_search_item = request.form['map_search_item']
        search_location = geolocator.geocode(map_search_item, exactly_one=False, limit=10)
        print(search_location)
        return render_template('map_search.html', footer_vars=footer_vars, search_results=search_location)

    else:
        return render_template('map_search.html', footer_vars=footer_vars)


