from django.urls import reverse
from rest_framework import status
from billjobs.tests.generics import GenericAPITest
import collections

class AnonymousPermissionAPITest(GenericAPITest):
    """
    Test /permissions endpoint status code and response data for anonymous user
    """

    def setUp(self):
        super().setUp()
        self.url = reverse('permissions-api')
        self.expected_status = {
                'GET': 401,
                'POST': 401,
                'PUT': 401,
                'DELETE': 401,
                'HEAD': 401,
                'OPTIONS': 401,
                'HEAD': 401,
                }

    def tearDown(self):
        super().tearDown()

    def test_permission_api_status_code(self):
        self.status_code_is()

