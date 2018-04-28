import random

from model.project import Project


def test_delete_project(app):
    if len(app.project.get_project_list()) == 0:
        app.project.create(Project(name="test", status="stable", view_status="private", description="some text"))

    old_projects = app.soap.get_project_list()
    project = random.choice(old_projects)
    app.project.delete(project.name)
    new_projects = app.soap.get_project_list()
    assert len(old_projects) - 1 == len(new_projects)
    old_projects.remove(project)
    assert sorted(old_projects, key=Project.get_name) == sorted(new_projects, key=Project.get_name)
