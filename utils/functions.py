## Global functions

import os
import random
from flask import session

def load_secret_key(data_dir):
    if not os.path.exists(os.path.join(data_dir, 'secret.key')):
        secret_key = os.urandom(32)
        with open(os.path.join(data_dir, 'secret.key'), 'wb') as file:
            file.write(secret_key)
            file.close()
        return secret_key
    else:
        with open(os.path.join(data_dir, 'secret.key'), 'rb') as file:
            secret_key = file.read()
            file.close()
        return secret_key


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

def exp_character(save_id, current_xp, level, earned_xp):
    level = int(level)
    required_xp = 1000
    # print(required_xp)
    # print(current_xp)
    # print(earned_xp)
    current_xp += earned_xp
    # print(current_xp)
    if current_xp >= required_xp:
        # level up !
        # print('level up')
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
        # print('not level up')
        session['current_xp'] = current_xp
        session['required_xp'] = required_xp
    return session
