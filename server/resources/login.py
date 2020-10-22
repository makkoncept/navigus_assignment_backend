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
        user = ''
        if args['role'] == 'student':
            user = StudentModel.query.filter_by(username=args['username']).first()
        elif args['role'] == 'teacher':
            user = TeacherModel.query.filter_by(username=args['username']).first()
        else:
            abort(422) # not a valid role

        if not user or user.password != args['password']:
            abort(401) # unauthorized

        return {'results': args}