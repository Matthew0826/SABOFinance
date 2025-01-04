from datetime import datetime
'''
This class handles all of the data for an account
This means the name and index of the account
'''
class Account:
    def __init__(self, account_code:str, budget_index:str):
        self._account_code = account_code
        self._budget_index = budget_index
    
    ''' GETTERS '''
    @property
    def account_code(self):
        return self._account_code
    @property
    def budget_index(self):
        return self._budget_index


