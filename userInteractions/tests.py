from django.test import TestCase

# Create your tests here.

from django.test import TestCase

from model_bakery import baker

from userInteractions.models import Review, Question


class ReviewTestModel(TestCase):

    def setUp(self):
        self.review = baker.make(Review, body="Il corso è stato molto interessante")

    def test_using_customer(self):
        self.assertEqual(self.review.body, "Il corso è stato molto interessante")

class QuestionTestModel(TestCase):

    def setUp(self):
        self.question = baker.make(Question)

    def test_using_customer(self):
        self.assertIsInstance(self.question, Question)
