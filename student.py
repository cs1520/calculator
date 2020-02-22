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


def read_student_info(datastore_client, student_id):
    student_key = datastore_client.key("Student", str(student_id))
    print("Searching for " + str(student_id))
    info = datastore_client.get(key=student_key)
    if info is None:
        return None
    s = Student(info["last_name"], info["first_name"], info["username"], student_id)
    return s
