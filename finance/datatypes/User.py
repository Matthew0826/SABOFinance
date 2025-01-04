'''
This class handles a frontend user trying to access data.
This is for security and ease-of-use reasons
'''
from typing import List
from datetime import datetime

class User:
    def __init__(self, nuid:str, token:str, time_last_used:datetime, permissions:List[str] = [], actions = {}):
        self._nuid = nuid
        self._token = token
        self._time_last_used = time_last_used
        self._permissions = permissions
        self._actions = actions

    @property
    def nuid(self):
        return self._nuid
    @property
    def token(self):
        return self._token
    @property
    def time_last_used(self):
        return self._time_last_used
    @property
    def permissions(self):
        return self._permissions
    @property
    def actions(self):
        return self._actions

    # Updates datetime to current
    def use(self):
        self._time_last_used = datetime.now()
