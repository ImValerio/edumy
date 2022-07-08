from django.test import TestCase

# Create your tests here.

from django.test import TestCase

from model_bakery import baker

from userAuth.models import UserType


class UserTestModel(TestCase):

    def setUp(self):
        self.users = baker.make('userAuth.UserType', _quantity=3)

    def test_using_customer(self):
        assert len(self.users) == 3
