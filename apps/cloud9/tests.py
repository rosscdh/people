# encoding: utf-8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import apps.cloud9 as cloud9

class Cloud9BaseTest(TestCase):
    def test_valid_domain(self):
        """
        Tests that a domain is alid according to `SOCIALREGISTRATION_ALLOWED_DOMAINS`
        """
        self.assertTrue(cloud9.is_valid_domain('adcloud.com'))

    def test_invalid_domain(self):
        """
        Tests that a domain is alid according to `SOCIALREGISTRATION_ALLOWED_DOMAINS`
        """
        self.assertTrue(cloud9.is_valid_domain('example.com'))

    def test_socialregistration_initial_data(self):
        """
        test the initial data returned from a mocked openid client
        client.result.message.getArgs() # mocked
        request, user, profile, client
        """
        pass

    def test_socialregistration_ax_request(self):
        """
        Test Appended AX request items need to mock theopenid url
        mocks ax.FetchRequest()
        """
        pass

    def test_parse_email(self):
        """
        Test that the parser returns a useable dict
        """
        email_dict = cloud9.parse_email('ross.crawford@adcloud.com')
        expected_dict = dict({
        'username': 'ross.crawford',
        'host': 'adcloud.com',
        })
        self.assertEqual(email_dict, expected_dict)

    def test_normalize_openid_keys(self):
        """
        Turns the namespaced openid tuple into a useable keyvalue hash
        """

class Cloud9AdcloudInfoModelTest(TestCase):
    def setup(self):
        from apps.cloud9.models import AdcloudInfo
        from django.contrib.auth.models import User
        self.user = User.objects.get(pk=1)
        self.AdcloudInfoObject = AdcloudInfo(
            user = self.user,
            department = AdcloudInfo.DEPARTMENTS.DEV,
            workplace = AdcloudInfo.OFFICES.COLOGNE,
        )

    def test_object_department_property(self):
        """ test the department property is set """
        self.assertEqual(self.AdcloudInfoObject.dept, 'Tech')

    def test_object_office_property(self):
        """ test the office property is set """
        self.assertEqual(self.AdcloudInfoObject.office, 'Köln')

        