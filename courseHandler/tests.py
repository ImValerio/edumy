# Create your tests here.

from django.test import TestCase

from model_bakery import baker

from courseHandler.models import Course


class CourseHandlerTestModel(TestCase):

    def test_create_course(self):
        self.course = baker.make(Course)
        self.assertIsInstance(self.course, Course)


