import os
from suds.client import Client
from suds import WebFault

from model.project import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def get_project_list(self):
        client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        projects = client.service.mc_projects_get_user_accessible("administrator", "root")
        parsed_projects = []
        for project in projects:
            parsed_projects.append(Project(name=project["name"], status=project["status"]["name"],
                                           view_status=project["view_state"]["name"], description=project["description"]))
        return parsed_projects
