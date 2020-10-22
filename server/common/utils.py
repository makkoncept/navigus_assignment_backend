from flask_restful import fields

user_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "password": fields.String,
    "auth_level": fields.String,
}

course_fields = {
    "id": fields.Integer,
    "course_code": fields.String,
    "name": fields.String,
}
