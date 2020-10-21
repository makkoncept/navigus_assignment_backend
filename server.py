from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

courses = {
    1: {"course_code": "HS481", "name": "Application of psychology"},
    2: {"course_code": "PE482", "name": "Health Safety & Environment in Industry"},
    3: {"course_code": "CS101", "name": "Introduction to Computer Science"},
}


def abort_if_course_id_not_exist(course_id):
    if course_id not in courses:
        abort(404, message=f"Course id: {course_id} does not exist")


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


api.add_resource(CourseList, "/courses/")
api.add_resource(Course, "/courses/<int:course_id>")

if __name__ == "__main__":
    app.run(debug=True)


# add a basic skeleton for course Resource

# used in memory dictionary for now