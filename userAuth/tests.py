# Create your tests here.

from django.test import TestCase

from model_bakery import baker


class UserAuthTestModel(TestCase):

    def test_create_user(self):
        self.users = baker.make('userAuth.UserType', _quantity=3)
        assert len(self.users) == 3
