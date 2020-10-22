from flask_cors import CORS
from flask_restful import Api, Resource, reqparse, abort, fields, marshal
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class StudentModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, index=True)
    password = db.Column(db.String(32), nullable=False)
    auth_level = db.Column(db.String(10), default="user")

    def __repr__(self):
        return f"{self.id} | {self.username} | {self.auth_level}"


class TeacherModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password = db.Column(db.String(32))
    auth_level = db.Column(db.String(10), default="admin")

    def __repr__(self):
        return f"{self.id} | {self.username} | {self.auth_level}"


courses = {
    1: {"course_code": "HS481", "name": "Application of psychology"},
    2: {"course_code": "PE482", "name": "Health Safety & Environment in Industry"},
    3: {"course_code": "CS101", "name": "Introduction to Computer Science"},
}

user_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "auth_level": fields.String,
}



def abort_if_course_id_not_exist(course_id):
    if course_id not in courses:
        abort(404, message=f"Course id: {course_id} does not exist")


class StudentList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "username",
            type=str,
            required=True,
            location="json",
        )
        self.reqparse.add_argument("password", type=str, required=True, location="json")
        super(StudentList, self).__init__()

    def get(self):
        students = StudentModel.query.all()
        return marshal(students, user_fields)

    def post(self):
        args = self.reqparse.parse_args()

        user = StudentModel(username=args["username"], password=args["password"])

        db.session.add(user)
        db.session.commit()

        return {"message": "posted"}


class TeacherList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "username",
            type=str,
            required=True,
            location="json",
        )
        self.reqparse.add_argument("password", type=str, required=True, location="json")
        super(TeacherList, self).__init__()

    def get(self):
        teachers = TeacherModel.query.all()
        return marshal(teachers, user_fields)

    def post(self):
        args = self.reqparse.parse_args()
        user = TeacherModel(username=args["username"], password=args["password"])

        db.session.add(user)
        db.session.commit()

        return {"message": "posted"}


class CourseList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "course_code",
            type=str,
            required=True,
            location="json",
        )
        self.reqparse.add_argument("name", type=str, required=True, location="json")
        super(CourseList, self).__init__()

    def get(self):
        return courses

    def post(self):
        args = self.reqparse.parse_args()
        courses[len(courses) + 1] = args
        return courses, 201


class Course(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("course_code", type=str, location="json")
        self.reqparse.add_argument("name", type=int, location="json")
        super(Course, self).__init__()

    def get(self, course_id):
        abort_if_course_id_not_exist(course_id)
        return courses[course_id]

    def put(self, course_id):
        abort_if_course_id_not_exist(course_id)
        args = self.reqparse.parse_args()
        for key, value in args.items():
            if value is not None:
                courses[course_id][key] = value

        return courses

    def delete(self, course_id):
        abort_if_course_id_not_exist(course_id)
        del courses[course_id]
        return courses, 204


api.add_resource(StudentList, "/students/")
api.add_resource(TeacherList, "/teachers/")
api.add_resource(CourseList, "/courses/")
api.add_resource(Course, "/courses/<int:course_id>")

if __name__ == "__main__":
    app.run(debug=True)
