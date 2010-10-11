"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from django.test.client import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from pub4me.models import Pub, City

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
        self._c = Client()
        load_test_data(TEST_CITY_ID, TEST_PL_NAME, TEST_EN_NAME, TEST_PUB_NAME, TEST_EXT_SERVICE_ID)

    """Testuje glowny widok zwracajacy Landing Page"""
    def test_index_view(self):
        response = self._c.post(reverse("PubsProject.pub4me.views.index"))
        self.assertNotEqual(None, response)
        self.assertEqual(200, response.status_code, "Index view failed to respond")


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




    



