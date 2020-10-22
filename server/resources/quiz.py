from flask_restful import Resource, reqparse, marshal, abort, fields

from server import db
from server.models import CourseModel, QuestionModel, OptionModel
from server.common.utils import question_fields


class Quiz(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        """ Due to the limitations of request parser, partial validation will be done here. It 
        validates that 'text' key which contains string exist and an 'options' key exists which
        should be a array of dictionary. The sanity check on the dictionary will be done while
        parsing it."""
        self.reqparse.add_argument(
            "text",
            type=str,
            required=True,
            location="json",
        )
        self.reqparse.add_argument(
            "options", type=dict, required=True, location="json", action="append"
        )
        super(Quiz, self).__init__()

    def get(self, course_id, question_no):
        course = CourseModel.query.filter_by(id=course_id).first()
        if course is None:
            abort(404, message=f"course with course id = {course_id} does not exist")

        questions = course.questions
        if len(questions) < question_no:
            abort(400)

        target_question = questions[question_no - 1]

        # print(questions)
        # return {"results": marshal(courses, course_fields)}
        return {"results": marshal(target_question, question_fields)}
