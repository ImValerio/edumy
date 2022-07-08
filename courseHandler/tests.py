from django.test import TestCase

# Create your tests here.

from django.test import TestCase

from model_bakery import baker

from courseHandler.models import Course


class CourseTestModel(TestCase):

    def setUp(self):
        self.course = baker.make(Course)

    def test_using_customer(self):
        self.assertIsInstance(self.course, Course)