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

class UserPermissionDetailAPITest(GenericAPITest):
    """
    Test /permissions/pk endpoint status code and response data for
    authenticated user
    """

    def setUp(self):
        super().setUp()
        self.url = reverse('permissions-detail-api', args=(1,))
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

    def test_permission_detail_api_status_code(self):
        self.status_code_is()

    def test_permission_detail_api_content(self):
        self.content_is()

class AdminPermissionAPITest(GenericAPITest):
    """
    Test /permissions endpoint status code and response data for authenticated
    admin
    """

    def setUp(self):
        super().setUp()
        self.url = reverse('permissions-api')
        self.force_authenticate(user=self.admin)
        self.expected_status = {
                'GET': 200,
                # POST is not tested because of an error with Django content
                # type object
#                'POST': 200,
                'PUT': 405,
                'DELETE': 405,
                'HEAD': 200,
                'OPTIONS': 200,
                'PATCH': 405,
                }
        self.expected_content = {
                'GET': [
                    collections.OrderedDict({
                        "url": "http://testserver/billjobs/api/1.0/permissions/1/",
                        "name": "Can add log entry",
                        "codename": "add_logentry"
                    }),
                    collections.OrderedDict({
                        "url": "http://testserver/billjobs/api/1.0/permissions/18/",
                        "name": "Can delete session",
                        "codename": "delete_session"
                        }),
                    ],
#                'POST': self.error_message['403'],
                'PUT': self.error_message['405_PUT'],
                'DELETE': self.error_message['405_DELETE'],
                # Do not test message
#                'HEAD': self.error_message['403'],
#                'OPTIONS': self.error_message['403'],
                'PATCH': self.error_message['405_PATCH'],
                }

    def tearDown(self):
        super().tearDown()

    def test_permission_api_status_code(self):
        self.status_code_is()

    def test_permission_api_content(self):
        self.content_is()

class AdminPermissionDetailAPITest(GenericAPITest):
    """
    Test /permissions/pk endpoint status code and response data for
    authenticated admin
    """

    def setUp(self):
        super().setUp()
        self.url = reverse('permissions-detail-api', args=(1,))
        self.force_authenticate(user=self.admin)
        self.expected_status = {
                'GET': 200,
                'POST': 405,
#                'PUT': 200,
#                'DELETE': 204,
#                'HEAD': 200,
#                'OPTIONS': 200,
#                'PATCH': 405,
                }
        self.expected_content = {
                'GET': {
                    "url": "http://testserver/billjobs/api/1.0/permissions/1/",
                    "name": "Can add log entry",
                    "codename": "add_logentry"
                    },
                'POST': self.error_message['405_POST'],
#                'PUT': self.error_message['405_PUT'],
#                'DELETE': self.error_message['405_DELETE'],
                # Do not test message
#                'HEAD': self.error_message['403'],
#                'OPTIONS': self.error_message['403'],
#                'PATCH': self.error_message['405_PATCH'],
                }

    def tearDown(self):
        super().tearDown()

    def test_permission_api_status_code(self):
        self.status_code_is()

    def test_permission_api_content(self):
        self.content_is()


