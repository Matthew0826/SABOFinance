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

    def get_options(self):
        return self._manager.get_options()

    # This activates when the webhook is called
    def on_webhook(self, sheet_name:str):
        self._manager.update()

    # This adds a request to the system
    def add_request(self, token:str, request:dict):
        user = self._manager.get_user(token)                # Get the user      
        self._manager.add_request(description=request['description'], requestee=request['requestee'], account_code=request['account_code'],
            budget_index=request['budget_index'], project_name=request['project_name'], subteam_name=request['subteam_name'], 
            request_cost=request['request_cost'], link=request['link'])
    
    # This submits the approval
    def add_approval(self, token:str, rqid:int, approval:dict):
        user = self._manager.get_user(token)                # Verify the token
        self._manager.add_approval(rqid=rqid, approval_status=approval['approved'] == 'true', approver=approval['user'], approval_level=approval['level'], notes=approval['note'])

    # This submits final information
    def add_final(self, token:str, rqid:int, final_info:dict):
        user = self._manager.get_user(token)
        self._manager.add_final(rqid=rqid, )
