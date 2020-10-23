from flask_restful import Resource, reqparse, abort

from server.models import TeacherModel, StudentModel


class Login(Resource):
    # method_decorators = {
    #     "get": [auth.login_required],
    #     "put": [permission_required("admin"), auth.login_required],
    #     "delete": [permission_required("admin"), auth.login_required],
    # }

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("username", type=str, location="json")
        self.reqparse.add_argument("password", type=str, location="json")
        self.reqparse.add_argument("role", type=str, location="json")
        super(Login, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        print(args)
        user = ""
        if args["role"] == "student":
            user = StudentModel.query.filter_by(username=args["username"]).first()
        elif args["role"] == "teacher":
            user = TeacherModel.query.filter_by(username=args["username"]).first()
        else:
            # not a valid role
            abort(422, message=f"{args['role']} is not a valid role")

        if not user:
            abort(404, message=f"{args['role']} with that username does not exist")

        if user.password != args["password"]:
            abort(401, message="Unauthorized: wrong password")  # unauthorized

        return {"results": args}
