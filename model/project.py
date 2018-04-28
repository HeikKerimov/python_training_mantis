class Project:

    def __init__(self, name=None, status=None, view_status=None, description=None):
        self.name = name
        self.status = status
        self.view_status = view_status
        self.description = description

    def __repr__(self):
        return "%s : %s" % (self.name, self.description)

    def __eq__(self, other):
        return self.name == other.name and self.status == other.status and self.description == self.description

    def get_name(self):
        return self.name