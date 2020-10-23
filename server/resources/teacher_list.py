from flask_restful import Resource, reqparse, marshal, abort

from server import db, auth
from server.models import TeacherModel
from server.common.utils import user_fields


class TeacherList(Resource):
    # method_decorators = [permission_required("admin"), auth.login_required]

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
        super(TeacherList, self).__init__()

    def get(self):
        teachers = TeacherModel.query.all()
        return marshal(teachers, user_fields)

    def post(self):
        args = self.reqparse.parse_args()

        # checking if the teacher already exists
        if TeacherModel.query.filter_by(username=args["username"]).first() is not None:
            abort(409, message="Teacher with this username already exists.")

        # the role is not correct for the teacher
        if args["role"] != "teacher":
            abort(400, message="bad request")  # bad request

        # the default auth_level for teacher is set to 'admin' in db model.
        # For students, the auth_level is 'user'. This field helps in doing role based
        # authentication. Some resources are to be exposed to the admin only.
        user = TeacherModel(username=args["username"], password=args["password"])

        db.session.add(user)
        db.session.commit()

        return {"results": marshal(user, user_fields)}
