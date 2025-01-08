'''
This class has a lot of fields. It manages everything for the request.
This is probably going to be really big. Oh well.
'''
from .Account import Account
from .Approval import Approval
from .Subteam import Subteam
from datetime import datetime

# Define the format of the date string
DATE_FORMAT = "%m/%d/%Y %H:%M:%S"

class Request:
    def __init__(self, **kwargs):
        ''' Go through kwargs and use each one (or keep default if not) '''
        self._id = int(kwargs['rqid']) if 'rqid' in kwargs else int(kwargs['id']) if 'id' in kwargs else -1
        self._description = kwargs['description'] if 'description' in kwargs else ''
        self._status = kwargs['status'] if 'status' in kwargs else ''
        self._requestee = kwargs['requestee'] if 'requestee' in kwargs else None        
        ''' Skip the more complicated variables because these have more conditions '''
        self._request_cost = kwargs['request_cost'].replace('$','') if 'request_cost' in kwargs else -1
        self._final_cost = kwargs['final_cost'].replace('$','') if 'final_cost' in kwargs else ''
        self._tax = kwargs['tax'].replace('$','') if 'tax' in kwargs else ''
        self._link = kwargs['link'] if 'link' in kwargs else ''
        self._reciept_link = kwargs['reciept_link'] if 'reciept_link' in kwargs else ''
        self._sabo_link = kwargs['sabo_link'] if 'sabo_link' in kwargs else ''
        self._request_date:datetime = Request.format_time(kwargs['request_date']) if 'request_date' in kwargs else datetime.now()
        self._submission_date:datetime = Request.format_time(kwargs['submission_date']) if 'submission_date' in kwargs else None

        ''' Parse approvals '''
        # Create empty dictionary to store approvals
        self._approvals = {}
        approval_categories = ['', 'admin', 'advisor']

        for category in approval_categories:
            #Format the category properly
            formatted_category = category + '_' if category != '' else category

            if formatted_category + 'approver' in kwargs:
                if formatted_category + 'approval_date' in kwargs:
                    self._approvals[category] = Approval(kwargs['approver'], Request.format_time(kwargs['approval_date']))
                else:
                    self._approvals = Approval(kwargs['approver'])
            elif formatted_category + 'approval' in kwargs:
                self._approvals[category] = kwargs['approval']

        ''' Parse subteam '''
        if 'project_name' in kwargs and 'subteam_name' in kwargs:
            self._subteam = Subteam(kwargs['project_name'], kwargs['subteam_name'])
        elif 'subteam' in kwargs:
            self._subteam = kwargs['subteam']
        else:
            self._subteam = None

        ''' Parse Account '''
        if 'budget_index' in kwargs and 'account_code' in kwargs:
            self._account = Account(kwargs['account_code'], kwargs['budget_index'])
        elif 'account' in kwargs:
            self._account = kwargs['account']
        else:
            self._account = None
    
    ''' Correctly Format the Time '''
    @staticmethod
    def format_time(time, to_datetime=True):
        if to_datetime:
            if time == '':
                return None
            else:
                return datetime.strptime(time, DATE_FORMAT)
        else:
            if time == None:
                return ''
            else:
                return str(time.strftime(DATE_FORMAT))

    ''' FORMATTING FUNCTION '''
    def to_dict(self):
        return {
            'id': self._id, 
            'description': self._description,
            'status': self._status,
            'requestee': self._requestee,
            'account_code': self._account.account_code,
            'budget_index': self._account.budget_index,
            'project_name': self._subteam.project_name,
            'subteam_name': self._subteam.subteam_name,
            'approver': self._approvals[''].approver if '' in self._approvals else '',
            'approval_date': Request.format_time(self._approvals[''].date, False) if '' in self._approvals else '',
            'admin_approver': self._approvals['admin'].approver if 'admin' in self._approvals else '',
            'admin_approval_date': Request.format_time(self._approvals['admin'].date, False) if 'admin' in self._approvals else '',
            'advisor_approver': self._approvals['advisor'] if 'advisor' in self._approvals else '',
            'advisor_approval_date': Request.format_time(self._approvals['advisor'].date, False) if 'advisor' in self._approvals else '',
            'request_cost': self._request_cost,
            'final_cost': self._final_cost,
            'tax': self._tax,
            'link': self._link,
            'reciept_link': self._reciept_link,
            'sabo_link': self._sabo_link,
            'request_date': Request.format_time(self._request_date, False),
            'submission_date': Request.format_time(self._submission_date, False)}
    
    ''' GETTERS '''
    def can_progress(self, name:str, permissions):
        if self.status == "Pending Approval" and (self.subteam.get_lead_permission() in permissions or self.subteam.get_admin_permission() in permissions):
            return True
        elif self.status == "Pending Admin Approval" and self.subteam.get_admin_permission() in permissions:
            return True
        elif self.status == "Approved" and self.requestee == name:
            return True
        else:
            return False

    def get_next_action(self):
        if self.status == "Pending Approval":
            return "Approve"
        elif self.status == "Pending Admin Approval":
            return "Approve as Admin"
        elif self.status == "Approved":
            return "Submit Reciept"
    
    @property
    def id(self):
        return self._id
    @property
    def description(self):
        return self._description
    @property
    def status(self):
        return self._status
    @property
    def requestee(self):
        return self._requestee
    @property
    def account(self):
        return self._account
    @property
    def subteam(self):
        return self._subteam
    @property
    def approval(self):
        return self._approvals['']
    @property
    def admin_approval(self):
        return self._approvals['admin']
    @property
    def advisor_approval(self):
        return self._approvals['advisor']
    @property
    def request_cost(self):
        return self._request_cost
    @property
    def final_cost(self):
        return self._final_cost
    @property
    def tax(self):
        return self._tax
    @property
    def link(self):
        return self._link
    @property
    def reciept_link(self):
        return self._reciept_link
    @property
    def sabo_link(self):
        return self._sabo_link
    @property
    def request_date(self):
        return self._request_date
    @property
    def submission_date(self):
        return self._submission_date
