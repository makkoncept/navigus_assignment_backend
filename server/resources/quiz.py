from flask_restful import Resource, reqparse, marshal, abort, fields

from server import db
from server.models import CourseModel, QuestionModel, OptionModel
from server.common.utils import question_fields


class Quiz(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "options", type=bool, required=True, location="json", action="append"
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

    def post(self, course_id, question_no):
        args = self.reqparse.parse_args()
        print(args, course_id, question_no)

        course = CourseModel.query.filter_by(id=course_id).first()
        if course is None:
            abort(404, message=f"course with course id = {course_id} does not exist")

        questions = course.questions
        if len(questions) < question_no:
            return {"results": "no question left"}

        target_question = questions[question_no - 1]
        options = target_question.options
        print(options)

        answers = []
        for option in options:
            if option.is_true:
                answers.append(True)
            else:
                answers.append(False)

        print(answers)
        return {"results": "received"}
