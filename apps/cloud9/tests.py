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
