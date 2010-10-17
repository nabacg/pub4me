from django.test.client import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from pub4me.models import Pub, City, PubUser

TEST_TERM = "Karlik"
TEST_PUB_NAME = TEST_TERM + "Pub"
TEST_CITY_ID = "1"
TEST_PL_NAME = "Dublin"
TEST_EN_NAME = TEST_PL_NAME
TEST_EXT_SERVICE_ID = 666
TEST_ERR_MSG_NAME = "err_msg"

def load_test_data(city_id, pl_name, en_name, pub_name, ext_id):
    test_city = City.objects.create(id = city_id, pl_name= pl_name, en_name=en_name)
    test_pub = Pub(name = pub_name, city = test_city, ext_service_id_kk = ext_id)
    test_pub.save()

class JsViewTest(TestCase):


    def setUp(self):
        if not hasattr(self, '_z'):
            self._c = Client()
        load_test_data(TEST_CITY_ID, TEST_PL_NAME, TEST_EN_NAME, TEST_PUB_NAME, TEST_EXT_SERVICE_ID)

    """Testuje glowny widok zwracajacy Landing Page"""
    def test_index_view(self):
        response = self._c.post(reverse("PubsProject.pub4me.views.index"))
        self.assertNotEqual(None, response)
        self.assertEqual(302, response.status_code, "Index view failed to respond")
        

    def test_valid_pub_search(self):
        response = self._c.get(reverse("PubsProject.pub4me.views.pub_autocomplete"), {"term": TEST_PUB_NAME})
        self.assertNotEqual(None, response)
        self.assertEqual(200, response.status_code, "Autocomplete view failed to respond")
        self.assertNotEqual(0, len(response.content))
        response_obj = eval(response.content)
        self.assertNotEqual(0, len(response_obj))

    def test_invalid_pub_search(self):
        response = self._c.post(reverse("PubsProject.pub4me.views.pub_autocomplete"))
        self.assertEqual(200, response.status_code, "Faktycznie aplikacja sie wywalila")
        response_obj = eval(response.content)
        err_msg = response_obj[TEST_ERR_MSG_NAME]
        self.assertNotEqual(None, err_msg)
        self.assertNotEqual(0, len(err_msg))

TEST_USERNAME = "GUTEK"
TEST_PASSWORD = "GUTEK"
TEST_EMAIL = "GUTEK@pub4.me"
SECOND_USERNAME = "KREMOS"
SECOND_PASSWORD = "KREMOS"
SECOND_EMAIL = "KREMOS@pub4.me"

def create_user(user_name, e_mail, pass_word):
    return PubUser.objects.create(username = user_name, password = pass_word, email = e_mail)

class AuthenticationViewTest(TestCase):

    def setUp(self):
        self._c = Client()

    def test_login_view_exists(self):
        response = self._c.get('/accounts/login/')
        self.assertNotEqual(None, response)
        self.assertEqual(200, response.status_code)
        
    def test_sign_up_view_exists(self):
        response = self._c.get(reverse("PubsProject.pub4me.views.sign_up"))
        self.assertNotEqual(None, response)
        self.assertEqual(200, response.status_code)

    def test_logged_user_gets_personalized_main_page(self):
        create_user(TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD)
        response = self._c.post(reverse("django.contrib.auth.views.login"), {"id_username": TEST_USERNAME, "id_password": TEST_PASSWORD})
        self.assertNotEqual(None, response)
        self.assertEqual(200, response.status_code)
        self.assertNotEqual(-1, response.content.find(TEST_USERNAME))
        
    def test_create_user_from_view(self):
        response = self._c.post(reverse("PubsProject.pub4me.views.sign_up"), {
                                                "id_username":  SECOND_USERNAME,
                                                "id_password":  SECOND_PASSWORD,
                                                "id_password2": SECOND_PASSWORD})
        self.assertEqual(200, response.status_code)
        created_user = PubUser.objects.filter(username = SECOND_USERNAME)
        self.assertNotEqual(0, len(created_user))


class UserCreation(TestCase):
    def test_create_pub_user(self):
        new_user = create_user(TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD)
        saved_user = PubUser.objects.get(pk = new_user.pk)
        print new_user, saved_user
        for attr in ["username", "email"]:
            self.assertEqual(unicode(getattr(new_user, attr)), getattr(saved_user, attr))




    



