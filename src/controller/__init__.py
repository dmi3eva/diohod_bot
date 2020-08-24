import os
import dill
from enum import Enum

from settings import *
from collections import defaultdict


class State(Enum):
    MENU = 0
    HELP = 1
    RESEARCH = 2
    NEWS = 3
    SETTINGS = 4

class Property(Enum):
    HISTORY = 0
    STATE = 1
    SHUTTLE = 2
    PLANET = 3
    EXECUTOR = 4
    NAME = 5


class UserState:
    def __init__(self, user_id=None):
        self.history = False
        self.state = State.MENU
        self.shuttle = None
        self.planet = None
        self.executor = None
        self.name = ANONYMOUS_USER
        self.id = user_id


class Controller:
    def __init__(self):
        self.users = defaultdict(UserState)
        existing_files = os.listdir(DB_DIR)
        if len(existing_files) > 0:
            existing_files_names = [os.path.join(DB_DIR, _f) for _f in existing_files]
            for user_file in existing_files_names:
                with open(user_file, 'rb') as db:
                    user_info = dill.load(db)
                    self.users[user_info.id] = user_info



    def get_user(self, user_id):
        if self.users[user_id].history:
            filename = self.get_user_file(user_id)
            with open(filename, 'rb') as db:
                try:
                    user = dill.load(db)
                    user.history = True
                    return user
                except KeyError:
                    return UserState(user_id)
        else:
            return self.users[user_id]

    def set_user(self, user_id, field: Property, value):
        if field is Property.NAME:
            self.users[user_id].name = value
            self.id = user_id
            filename = self.get_user_file(user_id)
            with open(filename, 'wb') as db:
                try:
                    dill.dump(self.users[user_id], db)
                except:
                    print('Что-то не записалось...')


    def get_user_file(self, user_id):
        return os.path.join(DB_DIR, '{}.dill'.format(str(user_id)))

    def restore_bd(self):
        for _id, _user in self.users.items():
            _user.id = _id
            filename = self.get_user_file(_id)
            with open(filename, 'wb') as user_file:
                dill.dump(_user, user_file)
