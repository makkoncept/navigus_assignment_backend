from flask_restful import Resource, reqparse, marshal, abort

from server import db, auth
from server.models import StudentModel
from server.common.utils import user_fields


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
        self.reqparse.add_argument("role", type=str, required=True, location="json")
        super(StudentList, self).__init__()

    def get(self):
        students = StudentModel.query.all()
        return {"results": marshal(students, user_fields)}

    def post(self):
        args = self.reqparse.parse_args()

        # checking if the student already exists
        if StudentModel.query.filter_by(username=args["username"]).first() is not None:
            abort(409)  # conflict

        # the role is not correct for the student
        if args["role"] != "student":
            abort(400)  # bad request

        # the auth_level is set as "user" by default
        user = StudentModel(username=args["username"], password=args["password"])

        db.session.add(user)
        db.session.commit()

        return {"results": marshal(user, user_fields)}
