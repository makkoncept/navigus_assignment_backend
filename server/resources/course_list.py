from flask_restful import Resource, reqparse, marshal

from server import db
from server.models import CourseModel
from server.common.utils import course_fields

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


