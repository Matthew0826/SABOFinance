'''
This class handles all of the managing of the finance system.
Most of the logic should be here. It interacts with the FinanceInterface class.
This class is meant to be secure. It does this by managing an active user list.
'''
from .interfaces.MFSInterface import MFSInterface

from .datatypes.User import User
from .datatypes.Student import Student
from .datatypes.Request import Request
import bcrypt, secrets, string
from datetime import datetime
import time

MINS_TO_EXPIRE = 5

class FinanceManager:
    def __init__(self):
        self._mfs_interface = MFSInterface()
        self._user_list = []
        self.update()
    
    ''' HELPER FUNCTIONS '''
    def _generate_actions(self, name:str, permissions ):
        actions = {}
        # Go through each request and see if there is anything they need to do
        for request in self.__request_dict.values():
            # Check if we can approve this user
            if request.can_progress(name, permissions):
                actions[request.id] = request.get_next_action()
        return actions

    ''' Store a user and get a token '''
    def generate_token(self, nuid:str, password:str) -> str:
        # Now check if there is no password
        hashed_password = self._mfs_interface.get_hashed_password(nuid)
        if hashed_password == '':
            return 'ERROR: No password set'
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            characters = string.ascii_letters + string.digits # Use letters & numbers
            token = ''.join(secrets.choice(characters) for _ in range(12))
            permissions = self._mfs_interface.get_permissions(nuid)
            user_name = ''
            for name, student in self.__student_dict.items():
                if student.id == nuid:
                    user_name = name
            self._user_list.append(User(nuid, token, datetime.now(), permissions, self._generate_actions(user_name, permissions)))
            return token
        else:
            return 'ERROR: Incorrect password'
    
    ''' Set the password '''
    def set_password(self, nuid:str, password:str):
        self._mfs_interface.set_hashed_password(nuid, bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))
    
    ''' Update the students and requests '''
    def update(self):
        # Generate the dictionaries of students & requests
        self.__student_dict = {}
        for key, value in self._mfs_interface.get_all_students().items():
            self.__student_dict[key] = Student(**value)

        self.__request_dict = {}
        for key, value in self._mfs_interface.get_all_requests().items():
            self.__request_dict[key] = Request(**value)
        
        # Get the options
        self.__options = self._mfs_interface.get_request_options()
        
    ''' Get the user from a token '''
    def get_user(self, token:str):
        # Go through each user in the user list
        for i in range(len(self._user_list)):

            # Remove the user if they are expired
            if (datetime.now() - self._user_list[i].time_last_used).total_seconds()/60 >= MINS_TO_EXPIRE:
                removed_token = self._user_list[i].token
                self._user_list.pop(i)

                # If we just removed our user, return an error
                if removed_token == token:
                    return "ERROR: User timed out"

            # If we found our user, return it
            if self._user_list[i].token == token:
                self._user_list[i].use()
                return self._user_list[i]

        return "ERROR: User not in list"

    ''' ACCESSOR CLASSES '''
    def get_user_info(self, user:User):
        return Student(**self._mfs_interface.get_student_info(user.nuid))

    def get_requests(self, user:User):
        # Get the raw request data
        request_dict = self._mfs_interface.get_requests_by_permissions(user.nuid, user.permissions)
        
        # Parse the request data into a list of Request objects
        requests = {}
        for request_id in request_dict.keys():
            requests[int(request_id)] = Request(**request_dict[request_id])
        return requests
    
    ''' MUTATOR CLASSES '''
    def add_request(self, description:str, requestee:str, account_code:str, budget_index:str, project_name:str, subteam_name:str):
        # Get the next index to use
        next_index = int(self.__requests.keys()[len(self.__requests()) - 1]) + 1
        
        # Create the new request
        self.__requests[next_index] = Request(rqid=next_id, description=description, requestee = requestee, account_code=account_code, budget_index=budget_index, project_name=project_name, subteam_name=subteam_name, request_date=datetime.now())

if __name__ == '__main__':
    fm = FinanceManager()
    token = fm.generate_token('002761220', 'turtle')
    print( 'Token generated: ', token)
    time.sleep(5)
    print(fm.get_user(token))
    time.sleep(5)
    print(fm.get_user(token))
    time.sleep(7)
    print(fm.get_user(token))
    time.sleep(3)
    print(fm.get_user(token))
