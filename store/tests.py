from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker


class TestSetUp(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.fake = Faker()

        self.user_data={
            'email': self.fake.email(),
            'username': self.fake.email().split('@')[0],
            'password': self.fake.email(),
        }

        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()
    

class TestViews(TestSetUp):
    def test_user_cannot_register_with_no_data(self):
        res=self.client.post(self.register_url)
        import pdb
        pdb.set_trace()
        self.assertEqual(res.status_code, 400)

    def test_user_can_register_correctly(self):
        res=self.client.post(self.register_url,self.user_data, format='json')
        self.assertEqual(res.status_code, 200)



