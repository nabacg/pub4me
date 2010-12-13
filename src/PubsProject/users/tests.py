from django.test.client import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
#from pub4me.models import Pub, City, PubUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.userfacade import create

TEST_USERNAME = "GUTEK"
TEST_PASSWORD = "GUTEK"
TEST_EMAIL = "GUTEK@pub4.me"
SECOND_USERNAME = "KREMOS"
SECOND_PASSWORD = "KREMOS"
SECOND_EMAIL = "KREMOS@pub4.me"

def create_user(user_name, e_mail, pass_word):
    return User.objects.create(username = user_name, password = pass_word, email = e_mail)

class AuthenticationViewTest(TestCase):

    def setUp(self):
        self._c = Client()

    def test_login_view_exists(self):
        response = self._c.get('/accounts/login/')
        self.assertNotEqual(None, response)
        self.assertEqual(200, response.status_code)

    def test_sign_up_view_exists(self):
        response = self._c.get(reverse("users.views.sign_up"))
        self.assertNotEqual(None, response)
        self.assertEqual(200, response.status_code)

    def test_logged_user_gets_personalized_main_page(self):
        user = create_user(TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD)
        response = self._c.post(reverse("django.contrib.auth.views.login"), {"username": TEST_USERNAME, "password": TEST_PASSWORD})
        self.assertNotEqual(None, response)
        self.assertEqual(200, response.status_code)
        self.assertNotEqual(-1, response.content.find(TEST_USERNAME))
        user.delete()

    def test_create_user_from_view(self):
        response = self._c.post(reverse("users.views.sign_up"), {
                                                "username":  SECOND_USERNAME,
                                                "password1": SECOND_PASSWORD,
                                                "password2": SECOND_PASSWORD})
        self.assertEqual(200, response.status_code)
        created_user = User.objects.filter(username = SECOND_USERNAME)
        self.assertNotEqual(0, len(created_user))
        created_user.delete()


class UserCreation(TestCase):
    def test_create_pub_user(self):
        new_user = create_user(TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD)
        saved_user = User.objects.get(pk = new_user.pk)
        for attr in ["username", "email"]:
            self.assertEqual(unicode(getattr(new_user, attr)), getattr(saved_user, attr))
        saved_user.delete()


class UserFacadeTest(TestCase):

    def test_create_user_from_form(self):
        sign_form = UserCreationForm({"username": TEST_USERNAME, "password1": TEST_PASSWORD, "password2": TEST_PASSWORD})
        new_user = create(sign_form.data['username'], sign_form.data['password1'])
        saved_user = User.objects.get(pk = new_user.pk)
        self.assertNotEqual(None, saved_user)
        self.assertEqual(TEST_USERNAME, saved_user.username)
        saved_user.delete()


    def test_create_user_from_json(self):
        json_request = {"username": TEST_USERNAME, "password": TEST_PASSWORD}
        new_user = create(json_request['username'], json_request['password'])
        saved_user = User.objects.get(pk = new_user.pk)
        self.assertNotEqual(None, saved_user)
        self.assertEqual(TEST_USERNAME, saved_user.username)
        saved_user.delete()

    def test_create_user_from_fcb(self):
        new_user = create(TEST_USERNAME, TEST_PASSWORD)
        saved_user = User.objects.get(pk = new_user.pk)
        self.assertNotEqual(None, saved_user)
        self.assertEqual(TEST_USERNAME, saved_user.username)
        saved_user.delete()

