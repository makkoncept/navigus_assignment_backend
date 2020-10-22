from flask_restful import Resource, reqparse, marshal

from server import db
from server.models import CourseModel
from server.common.utils import course_fields
from server.helpers import abort_if_course_id_not_exist


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
