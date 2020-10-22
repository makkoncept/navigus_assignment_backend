from functools import wraps
from flask_restful import abort
from flask import g

from server import auth


from server.models import CourseModel, StudentModel, TeacherModel


def abort_if_course_id_not_exist(course_id):
    course = CourseModel.query.filter_by(id=course_id).first()
    if not course:
        abort(404, message=f"Course id: {course_id} does not exist")
    return course


@auth.verify_password
def verify_password(username, password):
    user = StudentModel.query.filter_by(username=username).first()
    print("inside")
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
