from model.project import Project
from generator.project import *


def test_add_project(app):

    project = Project(name="test", status="stable", view_status="private", description="some text")
    old_projects = app.project.get_project_list()
    while project in old_projects:
        project.name = random_string(project.name, 4)

    app.project.create(project)
    new_projects = app.project.get_project_list()
    old_projects.append(project)
    assert old_projects == new_projects
