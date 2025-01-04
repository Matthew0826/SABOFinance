'''
This class handles everything finance-related. This is the abstract level, these are mostly wrappers.
Use this class on the API to interact with the finance system.
DO NOT use other classes (i.e. FinanceManager) outside of here.
'''
from finance.FinanceManager import FinanceManager

class FinanceInterface:
    # This class is the interface for the finance system
    def __init__(self):
        self._manager = FinanceManager()
    
    # This signs in with the nuid and password and returns a token
    def sign_in(self, nuid:str, password:str) -> str:
        token = self._manager.generate_token(nuid, password)
        actions = self._manager.get_user(token).actions
        return {'token': token, 'actions': actions}

    def get_user_info(self, token:str):
        return self._manager.get_user_info(self._manager.get_user(token)).to_dict()
    
    def get_visible_requests(self, token:str):
        user = self._manager.get_user(token)
        request_list = self._manager.get_requests(user)
        return dict(zip(request_list.keys(), [request.to_dict() for request in list(request_list.values())]))
    
    def get_request(self, rqid:int, token:str):
        return self.get_visible_requests(token)[rqid]

    # This activates when the webhook is called
    def on_webhook(self, sheet_name:str):
        self._manager.update()
