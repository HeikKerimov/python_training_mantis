from model.project import Project
from generator.project import *


def test_add_project(app):

    project = Project(name="test", status="stable", view_status="private", description="some text")
    old_projects = app.soap.get_project_list()
    while project in old_projects:
        project.name = random_string(project.name, 5)

    app.project.create(project)
    new_projects = app.soap.get_project_list()
    old_projects.append(project)
    assert sorted(old_projects, key=Project.get_name) == sorted(new_projects, key=Project.get_name)
