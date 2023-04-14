from flask import Flask
from flask import render_template, request, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFProtect
from functools import wraps
from geopy.geocoders import Nominatim
from utils.vars import global_vars, footer_vars, session
import json
import logging
import os
import pathlib
import psutil
import requests
import requests
import utils.db as db
import utils.functions as f

## set variables

current_path = pathlib.Path(__file__).parent.absolute()
data_path = os.path.join(current_path, 'data')
log_path = os.path.join(current_path, 'logs')
save_file = os.path.join(data_path, 'save.db')
game_file = os.path.join(data_path, 'game.db')
log_file = os.path.join(log_path, 'app.log')
repository_owner = 'Wivik'
repository_name = 'pyp-boy'

PYP_BOY_LOG_LEVEL = os.environ.get('PYP_BOY_LOG_LEVEL')

if PYP_BOY_LOG_LEVEL is not None and PYP_BOY_LOG_LEVEL == 'DEBUG':
    log_level = 'DEBUG'
else:
    log_level = 'INFO'

## Create dir
if not os.path.isdir(log_path):
    try:
        os.mkdir(log_path)
    except:
        print('Fatal error : could not create log dir ?', (log_path,))
        raise

if not os.path.isdir(data_path):
    try:
        os.mkdir(data_path)
    except:
        print('Fatal error : could not create data dir ?', (data_path,))
        raise

## Start logger
log = logging.getLogger(global_vars['app_name'])
log_handler = logging.FileHandler(log_file)
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_format)
log.addHandler(log_handler)
if log_level == 'DEBUG':
    log.setLevel(logging.DEBUG)
else:
    log.setLevel(logging.INFO)

## Start flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
csrf = CSRFProtect()
csrf.init_app(app)
geolocator = Nominatim(user_agent="pyp-boy")

def check_session(f):
    @wraps(f)
    def decorated_check_session(*args, **kwargs):
        if 'save_id' not in session:
            return redirect(url_for('sys'))
        return f(*args, **kwargs)
    return decorated_check_session

@app.route("/")
def root():
    # create save file if missing
    db.create_save_database(save_file)
    # check if story db is present
    if not os.path.exists(game_file):
        # get the latest release
        get_release = f.get_latest_release(repository_owner, repository_name, game_file)
        return render_template('db.html', footer_vars=footer_vars, global_vars=v.global_vars, get_release=get_release, new=False)
    else:
        ## check new version
        db_version = db.get_game_db_version(game_file)
        global_vars['app_version'] = db_version['version']
        # print(db_version['version'])
        check_version = f.check_new_version(db_version, repository_owner, repository_name)
        if check_version:
            return render_template('db.html', footer_vars=footer_vars, global_vars=global_vars, new=True)
        else:
            return redirect(url_for('sys'))

@app.route("/newfile")
def root_new():
    # delete current game db and download it
    os.remove(game_file)
    f.get_latest_release(repository_owner, repository_name, game_file)
    db_version = db.get_game_db_version(game_file)
    global_vars['app_version'] = db_version['version']
    return redirect(url_for('sys'))

@app.route("/sys")
@app.route("/sys/load/<int:save_id>")
def sys(save_id=0):
    try_test_save_file = f.test_save_file(save_file)
    log.debug(try_test_save_file)
    save_data = None
    read_save = None
    if try_test_save_file:
        save_data = db.list_save_data(save_file)
    if save_id != 0:
        read_save = db.get_save_data(save_file, save_id)
    return render_template('sys/sys.html', footer_vars=footer_vars, global_vars=global_vars, try_test_save_file=try_test_save_file, save_data=save_data, read_save=read_save)

@app.route("/sys/load/save/<int:save_id>")
def sys_load_save(save_id):
    save_data = db.get_save_data(save_file, save_id)

    global session

    session = f.register_session(save_data['id'], name=save_data['name'], current_xp=save_data['current_xp'], level=save_data['level'], current_chapter=save_data['current_chapter'], current_step=save_data['current_step'])

    return redirect(url_for('data'))

@app.route("/sys/create")
def sys_create():
    db.create_save_database(save_file)
    return redirect(url_for('sys'))

@app.route("/sys/new", methods=('GET', 'POST'))
def sys_new():
    if request.method == 'POST':
        ret = db.create_character(save_file, character_name=request.form['sys_new_character'], gender=request.form['sys_new_gender'])
        if ret is None:
            return redirect(url_for('sys'))
        else:
            error_number = f.gen_random_hex_number()
            flash(error_number + ' CREATE_CHARACTER '+str(ret))
            return redirect(url_for('sys'))
    else:
        return render_template('sys/new.html', global_vars=global_vars)

@app.route("/stat")
def stat():
    test_save_file = f.test_save_file(save_file)
    return render_template('stat/stat.html', global_vars=global_vars, test_save_file=test_save_file)

@app.route("/inv")
@app.route("/inv/<inv_category>")
@app.route("/inv/<inv_category>/<int:item_id>")
@check_session
def inv(item_id=None, inv_category=None):

    if inv_category is None:
        return redirect(url_for('inv', inv_category='weapon'))

    if item_id is not None:
        inv_item = db.get_item(game_file, inv_category, item_id)
        selected_item = inv_item
        selected_item_type = inv_category
    else:
        selected_item = None
        selected_item_type = None
    inventory = db.get_inventory(save_file, session['save_id'], filter=inv_category)
    items = []
    for item in inventory:
        items.append(item['item_id'])
    inv_items = db.get_inv_items(game_file, items, inv_category)

    return render_template('inv/inv.html', global_vars=global_vars, inv_category=inv_category, inventory=inv_items, selected_item=selected_item, selected_item_type=selected_item_type)

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
    return render_template('map/map.html', location=location, global_vars=global_vars)

@app.route("/map/search", methods=('GET', 'POST'))
def map_search():
    if request.method == 'POST':
        map_search_item = request.form['map_search_item']
        search_location = geolocator.geocode(map_search_item, exactly_one=False, limit=10)
        print(search_location)
        return render_template('map/map_search.html', search_results=search_location, global_vars=global_vars)

    else:
        return render_template('map/map_search.html', global_vars=global_vars)


@app.route("/data")
@check_session
def data():
    save_data = db.get_save_data(save_file, session['save_id'])
    ## If it's the first chapter, register it in the path
    if save_data['current_chapter'] == 1 and save_data['current_step'] == 1:
        db.save_story_path(save_file, session['save_id'], 1, 1)
    chapter_and_step = db.get_chapter_step(game_file, save_data['current_chapter'], save_data['current_step'])

    return render_template('data/data.html', global_vars=global_vars, chapter_and_step=chapter_and_step)

@app.route("/data/chapter/<int:chapter_id>/step/<int:step_id>/next-chapter/<int:next_chapter>/choice/<int:choice_id>/exp/<int:exp>")
@check_session
def data_choice(chapter_id, step_id, next_chapter, choice_id, exp):

    global session

    exp_char = f.exp_character(session['current_xp'], session['level'], exp)
    session = exp_char

    url_params = request.args
    print('url args')
    print(url_params['loot'])
    loot = url_params['loot']
    if loot != 'None':
        db.loot(save_file, session['save_id'], loot)

    if chapter_id != next_chapter:
        chapter = next_chapter
        step = choice_id
    else:
        chapter = chapter_id
        step = choice_id

    chapter_and_step = db.get_chapter_step(game_file, chapter, step)

    db.save_progress(save_file, session['save_id'], chapter=chapter_and_step['chapter'], step=choice_id, level=session['level'], current_xp=session['current_xp'], end=chapter_and_step['end'])

    db.save_story_path(save_file, session['save_id'], chapter_and_step['chapter'], choice_id)

    return redirect(url_for('data'))

@app.route("/data/log")
@check_session
def data_log():
    story_path = db.get_story_path(save_file, session['save_id'])

    story = []
    for story_row in story_path:
        story_step = db.get_chapter_step(game_file, story_row['chapter'], story_row['step'])
        story.append(story_step['text'])
    return render_template('data/log.html', global_vars=global_vars, story=story)
