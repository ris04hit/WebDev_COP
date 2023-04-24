# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.account import Account  # noqa: E501
from swagger_server.models.id_institution_id import IdInstitutionId  # noqa: E501
from swagger_server.models.institution import Institution  # noqa: E501
from swagger_server.test import BaseTestCase


class TestInstitutionController(BaseTestCase):
    """InstitutionController integration test stubs"""

    def test_add_institution(self):
        """Test case for add_institution

        Add a new Institution to the database
        """
        body = Institution()
        response = self.client.open(
            '/Institution',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_institution_by_id(self):
        """Test case for get_institution_by_id

        Find Institution by ID
        """
        response = self.client.open(
            '/Institution/{Id}'.format(id=IdInstitutionId()),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_institution_by_name(self):
        """Test case for get_institution_by_name

        Find Institution by Name
        """
        response = self.client.open(
            '/Institution/{Name}'.format(name='name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_institution(self):
        """Test case for update_institution

        Update an existing Institution
        """
        body = Institution()
        response = self.client.open(
            '/Institution',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
