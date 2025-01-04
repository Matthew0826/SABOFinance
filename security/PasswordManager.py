import hashlib
import secrets
from datetime import datetime, timedelta

'''
This class handless all password management in the backend
This is used on a sign in and when information is protected
Passwords are stored hashed in the excel spreadsheet
Users are stored in a dict with their token
'''

#The number of minutes until the token expires
TIME_UNTIL_EXPIRATION = 5

curr_users:dict = {}

'''
This class stores information about a user
'''
class User:
    def __init__(self, username:str):
        self.username = username
        self.time_last_used = datetime.now()

'''
This verifies to check if the token is valid
'''
async def verify_token(token:str) -> bool:
    if token in curr_users:
        #Check if the user has not expired
        if (datetime.now() - curr_users[token].time_last_used) >= timedelta(minutes=TIME_UNTIL_EXPIRATION):
            curr_users[token].time_last_used = datetime.now()
            return True
    return False

'''
Returns the username associated with the token.
If the token is invalid, returns a blank string.
'''
async def get_user_from_token(token:str) -> str:
    if verify_token(token):
        return curr_users[token].username
    return ''

'''
Generates a hash string for a given password
'''
def generate_hash(input_string: str) -> str:
    # Create a SHA-256 hash object
    hash_object = hashlib.sha256()
    
    # Encode the input string and update the hash object
    hash_object.update(input_string.encode('utf-8'))
    
    # Convert the hash to a hexadecimal string
    hash_string = hash_object.hexdigest()
    return hash_string


# Example usage
input_string = "Hello, world!"
hash_result = generate_hash(input_string)
print(f"Input: {input_string}")
print(f"Hash: {hash_result}")
