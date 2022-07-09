# Create your tests here.

from django.test import TestCase

from model_bakery import baker

from userInteractions.models import Review, Question


class UserInteractionsTestModel(TestCase):

    def test_create_review(self):
        self.review = baker.make(Review, body="Il corso è stato molto interessante")
        self.assertEqual(self.review.body, "Il corso è stato molto interessante")

    def test_create_question(self):
        self.question = baker.make(Question)
        self.assertIsInstance(self.question, Question)

