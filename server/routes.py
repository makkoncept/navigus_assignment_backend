from server import api
from server.resources.student_list import StudentList
from server.resources.teacher_list import TeacherList
from server.resources.course_list import CourseList
from server.resources.course import Course
from server.resources.login import Login
from server.resources.quiz_list import QuizList
from server.resources.quiz import Quiz


api.add_resource(StudentList, "/students/")
api.add_resource(TeacherList, "/teachers/")
api.add_resource(CourseList, "/courses/")
api.add_resource(Course, "/courses/<int:course_id>")
api.add_resource(Login, "/login/")
api.add_resource(QuizList, "/quiz/<int:course_id>")
api.add_resource(Quiz, "/quiz/<int:course_id>/<int:question_no>")
