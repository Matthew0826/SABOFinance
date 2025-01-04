'''
This class stores project and subteam info
'''
class Subteam:
    def __init__(self, project_name:str, subteam_name:str):
        self._project_name = project_name
        self._subteam_name = subteam_name
    ''' GETTERS '''
    def get_lead_permission(self):
        return "(" + self.project_name + ") " + self.subteam_name + " Lead"
    def get_admin_permission(self):
        return self.project_name + " Admin"
    @property
    def project_name(self):
        return self._project_name
    @property
    def subteam_name(self):
        return self._subteam_name
