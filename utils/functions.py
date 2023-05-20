## Global functions

import os
import random
from flask import session
import requests
import json

def test_save_file(save_file, logger):
    """ Ensure save file is present, redirect to the sys tab if not """
    if os.path.exists(save_file):
        logger.debug('save false exists')
        return True
    else:
        logger.debug('save false does not exist')
        return False


def gen_random_hex_number():
    num_digits = 6
    hex_num = hex(random.randint(0, 16**num_digits - 1))[2:].upper()
    return hex_num

def register_session(save_id, logger, **kwargs):
    session['save_id'] = save_id
    session['character_name'] = kwargs.get('name')
    session['current_xp'] = kwargs.get('current_xp')
    session['level'] = kwargs.get('level')
    session['current_chapter'] = kwargs.get('current_chapter')
    session['current_step'] = kwargs.get('current_step')
    session['required_xp'] = 1000
    logger.debug(session)
    return session

def exp_character(current_xp, level, earned_xp, logger):
    level = int(level)
    required_xp = 1000
    current_xp += earned_xp
    logger.debug('current_xp = ' + str(current_xp))
    if current_xp >= required_xp:
        # level up !
        level += 1
        logger.debug('new level ' + str(level))
        session['level'] = level
        # get back the over xp
        change_xp = int(current_xp) - int(required_xp)
        if change_xp > 0:
            session['current_xp'] = change_xp
        else:
            session['current_xp'] = 0
        logger.debug('change_xp = '+ str(change_xp))
    # calculate new required xp
    else:
        session['current_xp'] = current_xp
        session['required_xp'] = required_xp
    return session

def check_new_version(current_version, owner, repo, logger):
    release_api=f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    logger.debug(release_api)
    response = requests.get(release_api)
    logger.debug(response)
    if response.ok:
        release = json.loads(response.content)
        release_version = release["tag_name"]
        current_version = 'v' + current_version['version']
        logger.debug(release_version)
        logger.debug(current_version)
        if release_version != current_version:
            logger.debug('new version')
            return True
        else:
            return False
    else:
        logger.warn('error while checking version')
        return False

def get_latest_release(owner, repo, game_file, logger):
    release_api=f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    logger.debug(release_api)
    response = requests.get(release_api)
    logger.debug(response)
    if response.ok:
        release = json.loads(response.content)
        asset_url = release["assets"][0]["browser_download_url"]
        response = requests.get(asset_url)
        if response.ok:
            with open(game_file, 'wb') as db:
                db.write(response.content)
                logger.info("db downloaded")
                return True
        else:
            logger.error("failed to download db")
            return False
    else:
        logger.error('failed to download db')
        return False

def get_app_version(version_file, logger):
    ver_file = open(version_file, 'r')
    version = json.load(ver_file)
    logger.debug(version['version'])
    version = str(version['version'])
    return version

