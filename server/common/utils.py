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

"""
Fields to serialize the complex response of question in quiz related routes
"""
option_fields = {
    "text": fields.String,
    "isTrue": fields.Boolean,
}

question_fields = {
    "text": fields.String,
    "options": fields.List(fields.Nested(option_fields)),
}
