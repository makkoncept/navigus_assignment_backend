from server import db

class StudentModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, index=True)
    password = db.Column(db.String(32), nullable=False)
    auth_level = db.Column(db.String(10), default="user")

    def __repr__(self):
        return f"{self.id} | {self.username} | {self.password} | {self.auth_level}"


class TeacherModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password = db.Column(db.String(32))
    auth_level = db.Column(db.String(10), default="admin")

    def __repr__(self):
        return f"{self.id} | {self.username} | {self.auth_level}"


class CourseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(10))
    name = db.Column(db.String(100))

    def __repr__(self):
        return f"{self.id} | {self.course_code} | {self.name}"
