from flask_restful import Resource, reqparse, marshal, abort

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
        return {"results": marshal(courses, course_fields)}

    def post(self):
        print("inside post")
        args = self.reqparse.parse_args()
        print(args)

        if (
            CourseModel.query.filter_by(course_code=args["course_code"]).first()
            is not None
        ):
            abort(409)  # conflict

        course = CourseModel(
            course_code=args["course_code"].lower(), name=args["name"].lower()
        )

        db.session.add(course)
        db.session.commit()

        return {"results": marshal(course, course_fields)}, 201
