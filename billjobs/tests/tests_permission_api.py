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
                'PATCH': 401,
                }
        self.expected_content = {
                'GET': self.error_message['401'],
                'POST': self.error_message['401'],
                'PUT': self.error_message['401'],
                'DELETE': self.error_message['401'],
                'HEAD': self.error_message['401'],
                'OPTIONS': self.error_message['401'],
                'PATCH': self.error_message['401'],
                }

    def tearDown(self):
        super().tearDown()

    def test_permission_api_status_code(self):
        self.status_code_is()

    def test_permission_api_content(self):
        self.content_is()

class AnonymousPermissionDetailAPITest(GenericAPITest):
    """
    Test /permissions/pk endpoint status code and response data for anonymous
    user
    """

    def setUp(self):
        super().setUp()
        self.url = reverse('permissions-detail-api', args=(1,))
        self.expected_status = {
                'GET': 401,
                'POST': 401,
                'PUT': 401,
                'DELETE': 401,
                'HEAD': 401,
                'OPTIONS': 401,
                'PATCH': 401,
                }
        self.expected_content = {
                'GET': self.error_message['401'],
                'POST': self.error_message['401'],
                'PUT': self.error_message['401'],
                'DELETE': self.error_message['401'],
                'HEAD': self.error_message['401'],
                'OPTIONS': self.error_message['401'],
                'PATCH': self.error_message['401'],
                }

    def tearDown(self):
        super().tearDown()

    def test_permission_detail_api_status_code(self):
        self.status_code_is()

    def test_permission_detail_api_content(self):
        self.content_is()

class UserPermissionAPITest(GenericAPITest):
    """
    Test /permissions endpoint status code and response data for authenticated
    user
    """

    def setUp(self):
        super().setUp()
        self.url = reverse('permissions-api')
        self.force_authenticate(user=self.bill)
        self.expected_status = {
                'GET': 403,
                'POST': 403,
                'PUT': 403,
                'DELETE': 403,
                'HEAD': 403,
                'OPTIONS': 403,
                'PATCH': 403,
                }
        self.expected_content = {
                'GET': self.error_message['403'],
                'POST': self.error_message['403'],
                'PUT': self.error_message['403'],
                'DELETE': self.error_message['403'],
                'HEAD': self.error_message['403'],
                'OPTIONS': self.error_message['403'],
                'PATCH': self.error_message['403'],
                }

    def tearDown(self):
        super().tearDown()

    def test_permission_api_status_code(self):
        self.status_code_is()

    def test_permission_api_content(self):
        self.content_is()
