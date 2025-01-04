'''
This class handles all approvals whether they be normal or admin
'''
from datetime import datetime

class Approval:
    ''' CONSTRUCTORS '''
    def __init__(self, approver:str):
        self._approver = approver
        self._date = datetime.now()
    def __init__(self, approver:str, date:datetime):
        self._approver = approver
        self._date = date

    ''' GETTERS '''
    @property
    def approver(self) -> str:
        return self._approver
    @property
    def date(self) -> datetime:
        return self._date
