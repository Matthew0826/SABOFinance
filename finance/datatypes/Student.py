'''
This class handles all data pertaining to a Student
'''
from .Subteam import Subteam

class Student:
    def __init__(self, **kwargs):
        self._id = kwargs['nuid'] if 'nuid' in kwargs else -1
        self._name = kwargs['name'] if 'name' in kwargs else ''
        self._email = kwargs['email'] if 'email' in kwargs else ''
        self._phone_number = kwargs['phone_number'] if 'phone_number' in kwargs else -1
        self._street = kwargs['street/po_box'] if 'street/po_box' in kwargs else ''
        self._city = kwargs['city'] if 'city' in kwargs else ''
        self._state = kwargs['state'] if 'state' in kwargs else ''
        self._zip = kwargs['zip_code'] if 'zip_code' in kwargs else ''
        self._password = kwargs['hashed_password'] if 'hashed_password' in kwargs else ''

        if 'project_name' in kwargs and 'subteam_name' in kwargs:
            self._subteam = Subteam(kwargs['project_name'], kwargs['subteam_name'])
        elif 'subteam' in kwargs:
            self._subteam = kwargs['subteam']
        else:
            self._subteam = None

        if 'permissions' not in kwargs:
            self._permissions = []
        elif type(kwargs['permissions']) == str:
            #Parse the string
            self._permissions = kwargs['permissions'].split('/')
            for i in range(len(self._permissions)):
                self._permissions[i] = self._permissions[i].strip()
        else:
            self._permissions = kwargs['permissions']

    ''' TO DICTIONARY '''
    def to_dict(self):
        if( len(self._permissions) == 0 ):
            permissions_str = ''
        else:
            permissions_str = self._permissions[0]
            for i in range(1,len(self._permissions)):
                permissions_str += (" / " + self._permissions[i])
        return {
            'nuid': self._id,
            'name': self._name,
            'email': self._email,
            'phone_number': self._phone_number,
            'street/po_box': self._street,
            'city': self._city,
            'state': self._state,
            'zip_code': self._zip,
            'hashed_password': self._password,
            'project_name': self._subteam.project_name,
            'subteam_name': self._subteam.subteam_name,
            'permissions': permissions_str}

    ''' GETTERS '''
    @property
    def id(self):
        return self._id
    @property
    def name(self):
        return self._name
    @property
    def email(self):
        return self._email
    @property
    def phone_number(self):
        return self._phone_number
    @property
    def street(self):
        return self._street
    @property
    def city(self):
        return self._city
    @property
    def state(self):
        return self._state
    @property
    def zip(self):
        return self._zip
    @property
    def subteam(self):
        return self._subteam
    @property
    def permissions(self):
        return self._permissions

