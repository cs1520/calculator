class Student:
    def __init__(self, last_name, first_name, username, id_num):
        self.last_name = last_name
        self.first_name = first_name
        self.username = username
        self.id_num = id_num

    @property
    def name(self):
        return self.first_name + " " + self.last_name

    @property
    def email(self):
        return self.username + "@pitt.edu"
