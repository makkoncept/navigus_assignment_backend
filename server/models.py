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
    course_code = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    passing_marks = db.Column(db.Integer, nullable=False)
    questions = db.relationship("QuestionModel", backref="course", lazy=True)

    def __repr__(self):
        return f"{self.id} | {self.course_code} | {self.name} | {self.questions}"


class QuestionModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text(), nullable=False)
    marks = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course_model.id"), nullable=False)
    options = db.relationship("OptionModel", backref="question", lazy=True)

    def __repr__(self):
        return f"{self.id} | {self.text} | {self.options}"


class OptionModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)
    isTrue = db.Column(db.Boolean, nullable=False)
    question_id = db.Column(
        db.Integer, db.ForeignKey("question_model.id"), nullable=False
    )

    def __repr__(self):
        return f"{self.id} | {self.text} | {self.question_id}"
