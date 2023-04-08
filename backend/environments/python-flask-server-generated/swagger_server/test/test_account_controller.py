# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.account import Account  # noqa: E501
from swagger_server.test import BaseTestCase


class TestAccountController(BaseTestCase):
    """AccountController integration test stubs"""

    def test_add_account(self):
        """Test case for add_account

        Add a new Account to the database
        """
        body = Account()
        response = self.client.open(
            '/Account',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_account(self):
        """Test case for delete_account

        Deletes Account from the database
        """
        response = self.client.open(
            '/Account',
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_account_by_id(self):
        """Test case for get_account_by_id

        Find Account by ID
        """
        response = self.client.open(
            '/Account/{Id}'.format(id=Account()),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_account_by_name(self):
        """Test case for get_account_by_name

        Find Account by Username
        """
        response = self.client.open(
            '/Account/{Username}'.format(username='username_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login_account(self):
        """Test case for login_account

        Logs Account into the system
        """
        query_string = [('username', 'username_example'),
                        ('password', 'password_example')]
        response = self.client.open(
            '/Account/login',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_logout_account(self):
        """Test case for logout_account

        Logs out current logged in Account session
        """
        response = self.client.open(
            '/Account/logout',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_account(self):
        """Test case for update_account

        Update an existing Account
        """
        body = Account()
        response = self.client.open(
            '/Account',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
