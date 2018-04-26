from model.project import Project


class ProjectHelper:

    project_cache = None

    def __init__(self, app):
        self.app = app

    def create(self, project):
        wd = self.app.wd
        self.open_manage_project_page()
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        self.fill_project_form(project)
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        self.project_cache = None

    def fill_project_form(self, project):
        wd = self.app.wd
        wd.find_element_by_name("name").click()
        wd.find_element_by_name("name").clear()
        wd.find_element_by_name("name").send_keys(project.name)
        wd.find_element_by_name("status").click()
        wd.find_element_by_xpath("//option[text()='%s']" % project.status).click()
        wd.find_element_by_name("view_state").click()
        wd.find_element_by_xpath("//option[text()='%s']" % project.view_status).click()
        wd.find_element_by_name("description").click()
        wd.find_element_by_name("description").clear()
        wd.find_element_by_name("description").send_keys(project.description)

    def open_manage_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/manage_overview_page.php") and len(wd.find_elements_by_class_name("form-title")) > 0):
            wd.find_element_by_link_text("Manage").click()

    def open_manage_project_page(self):
        wd = self.app.wd
        self.open_manage_page()
        if not (wd.current_url.endswith("/manage_proj_page.php") and len(wd.find_elements_by_xpath("//input[@value='Create New Project']")) > 0):
            wd.find_element_by_link_text("Manage Projects").click()

    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.open_manage_project_page()
            self.project_cache = []
            for element in wd.find_elements_by_xpath("//table[@class='width100']//tr[contains(@class, 'row-') and not(contains(@class, 'category'))]"):
                name = element.find_element_by_xpath("td[1]").text
                status = element.find_element_by_xpath("td[2]").text
                view_status = element.find_element_by_xpath("td[4]").text
                description = element.find_element_by_xpath("td[5]").text
                self.project_cache.append(Project(name=name, status=status, view_status=view_status, description=description))
        return list(self.project_cache)
