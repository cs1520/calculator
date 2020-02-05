import csv
from google.cloud import datastore

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


def main():
    students = list()    

    with open('student_info.csv', newline='') as csvfile:
        r = csv.reader(csvfile, delimiter=',')
        headers = next(r)
        for row in r:
            s = Student(row[0], row[1], row[2], row[3])
            students.append(s)
    
    client = datastore.Client()
    student_entities = list()
    for s in students:
        print(s.id_num + ": " + s.name + " " + s.email)
        student_key = client.key("Student", str(s.id_num))
        student_entity = datastore.Entity(key=student_key)
        student_entity["last_name"] = s.last_name
        student_entity["first_name"] = s.first_name
        student_entity["username"] = s.username
        student_entities.append(student_entity)
    client.put_multi(student_entities)


if __name__ == '__main__':
    main()