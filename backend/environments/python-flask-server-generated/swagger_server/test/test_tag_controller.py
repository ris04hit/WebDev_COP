# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.account import Account  # noqa: E501
from swagger_server.models.id_tag_id import IdTagId  # noqa: E501
from swagger_server.models.tag import Tag  # noqa: E501
from swagger_server.test import BaseTestCase


class TestTagController(BaseTestCase):
    """TagController integration test stubs"""

    def test_add_tag(self):
        """Test case for add_tag

        Add a new Tag to the database
        """
        body = Tag()
        response = self.client.open(
            '/Tag',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_tag_by_id(self):
        """Test case for get_tag_by_id

        Find Tag by ID
        """
        response = self.client.open(
            '/Tag/{Id}'.format(id=IdTagId()),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_tag_by_name(self):
        """Test case for get_tag_by_name

        Find Tag by Name
        """
        response = self.client.open(
            '/Tag/{Name}'.format(name='name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_tag(self):
        """Test case for update_tag

        Update an existing Tag
        """
        body = Tag()
        response = self.client.open(
            '/Tag',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
