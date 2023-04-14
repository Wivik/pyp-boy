## Global functions

import os
import random
from flask import session
import requests
import json

def test_save_file(save_file):
    """ Ensure save file is present, redirect to the sys tab if not """
    if os.path.exists(save_file):
        return True
    else:
        return False


def gen_random_hex_number():
    num_digits = 6
    hex_num = hex(random.randint(0, 16**num_digits - 1))[2:].upper()
    return hex_num

def register_session(save_id, **kwargs):
    session['save_id'] = save_id
    session['character_name'] = kwargs.get('name')
    session['current_xp'] = kwargs.get('current_xp')
    session['level'] = kwargs.get('level')
    session['current_chapter'] = kwargs.get('current_chapter')
    session['current_step'] = kwargs.get('current_step')
    session['required_xp'] = 1000

    return session

def exp_character(current_xp, level, earned_xp):
    level = int(level)
    required_xp = 1000
    current_xp += earned_xp
    if current_xp >= required_xp:
        # level up !
        level += 1
        session['level'] = level
        # get back the over xp
        change_xp = int(current_xp) - int(required_xp)
        if change_xp > 0:
            session['current_xp'] = change_xp
        else:
            session['current_xp'] = 0
    # calculate new required xp
    else:
        session['current_xp'] = current_xp
        session['required_xp'] = required_xp
    return session

def check_new_version(current_version, owner, repo):
    release_api=f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    response = requests.get(release_api)
    if response.ok:
        release = json.loads(response.content)
        release_version = release["tag_name"]
        current_version = 'v' + current_version['version']
        print(release_version)
        print(current_version)
        if release_version != current_version:
            print('new version')
            return True
        else:
            return False
    else:
        print('error while checking version')
        return False

def get_latest_release(owner, repo, game_file):
    release_api=f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    response = requests.get(release_api)
    if response.ok:
        release = json.loads(response.content)
        asset_url = release["assets"][0]["browser_download_url"]
        response = requests.get(asset_url)
        if response.ok:
            with open(game_file, 'wb') as db:
                db.write(response.content)
                print("db downloaded")
                return True
        else:
            print("failed to download db")
            return False
    else:
        print('failed to download db')
        return False

def get_app_version(version_file):
    ver_file = open(version_file, 'r')
    version = json.load(ver_file)
    # print(version['version'])
    version = str(version['version'])
    return version

