# Create your tests here.

from django.test import TestCase

from model_bakery import baker


class UserTestModel(TestCase):

    def test_using_user(self):
        self.users = baker.make('userAuth.UserType', _quantity=3)
        assert len(self.users) == 3
