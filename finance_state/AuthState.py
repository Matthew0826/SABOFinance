
import secrets
import datetime
import pytz

#This class handles all of the auth states and authentification requests
class AuthState:
    #Default init.
    def __init__( self, timeout = 5 ):
        self.timeout = timeout
        self.__user_dict = {}

    #This is the sign in function. It will return null if sign in failed or the key. (This key will expire)
    def sign_in( self, nuid ):
        if( nuid in self.__user_dict.keys ):
            return
