from flask_restful import Resource, reqparse, marshal, abort, fields

from server import db
from server.models import CourseModel, QuestionModel, OptionModel
from server.common.utils import question_fields


class QuizList(Resource):
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
        super(QuizList, self).__init__()

    # helper route. Will be removed in production
    def get(self, course_id):
        course = CourseModel.query.filter_by(id=course_id).first()
        if course is None:
            abort(404, message=f"course with course id = {course_id} does not exist")

        questions = course.questions
        print(questions)
        # return {"results": marshal(courses, course_fields)}
        return {"results": "done"}

    def post(self, course_id):
        print("inside post")
        args = self.reqparse.parse_args()
        print(args)

        course = CourseModel.query.filter_by(id=course_id).first()
        if course is None:
            abort(404, message=f"course with course id = {course_id} does not exist")

        question = QuestionModel(text=args["text"], course_id=course_id)

        for option in args["options"]:
            if (
                "text" not in option
                or "isTrue" not in option
                or not isinstance(option["text"], str)
                or not isinstance(option["isTrue"], bool)
            ):
                abort(400)
            else:
                db_option = OptionModel(text=option["text"], isTrue=option["isTrue"])
                question.options.append(db_option)

        db.session.add(question)
        db.session.commit()

        return {"results": marshal(question, question_fields)}
