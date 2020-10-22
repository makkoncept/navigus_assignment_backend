from functools import wraps

from flask import Flask, g
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse, abort, fields, marshal
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)
auth = HTTPBasicAuth()
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


class CourseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(10))
    name = db.Column(db.String(100))

    def __repr__(self):
        return f"{self.id} | {self.course_code} | {self.name}"

user_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "auth_level": fields.String,
}

course_fields = {
    "id": fields.Integer,
    "course_code": fields.String,
    "name": fields.String,
}

@auth.verify_password
def verify_password(username, password):
    user = StudentModel.query.filter_by(username=username).first()
    print('inside')
    print(user)
    if not user:
        user = TeacherModel.query.filter_by(username=username).first()
        if not user or not user.password == password:
            return False
    elif not user.password == password:
        return False

    g.user = user
    return True


def permission_required(auth_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if g.user.auth_level != auth_level:
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def abort_if_course_id_not_exist(course_id):
    course = CourseModel.query.filter_by(id=course_id).first()
    if not course:
        abort(404, message=f"Course id: {course_id} does not exist")
    return course


class StudentList(Resource):
    method_decorators = {
        "get": [auth.login_required],
    }

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
        return {'results': marshal(students, user_fields)}

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
        courses = CourseModel.query.all()
        return {'results': marshal(courses, course_fields)}

    def post(self):
        args = self.reqparse.parse_args()
        print(args)

        # TODO: handle if course code already exists

        course = CourseModel(course_code=args["course_code"].lower(), name=args["name"].lower())

        db.session.add(course)
        db.session.commit()

        return {'results': marshal(course, course_fields)}, 201


class Course(Resource):
    # method_decorators = {
    #     "get": [auth.login_required],
    #     "put": [permission_required("admin"), auth.login_required],
    #     "delete": [permission_required("admin"), auth.login_required],
    # }

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("course_code", type=str, location="json")
        self.reqparse.add_argument("name", type=str, location="json")
        super(Course, self).__init__()

    def get(self, course_id):
        course = abort_if_course_id_not_exist(course_id)
        return {'results': marshal(course, course_fields)}

    def put(self, course_id):
        course = abort_if_course_id_not_exist(course_id)
        args = self.reqparse.parse_args()
        print(args)
        for key, value in args.items():
            if value is not None:
                setattr(course, key, value)
        db.session.commit()
        print(course)
        return {'results': marshal(course, course_fields)}

    def delete(self, course_id):
        course = abort_if_course_id_not_exist(course_id)
        db.session.delete(course)
        db.session.commit()
        courses = CourseModel.query.all()
        return {'results': marshal(courses, course_fields)}, 204


api.add_resource(StudentList, "/students/")
api.add_resource(TeacherList, "/teachers/")
api.add_resource(CourseList, "/courses/")
api.add_resource(Course, "/courses/<int:course_id>")

if __name__ == "__main__":
    app.run(debug=True)
