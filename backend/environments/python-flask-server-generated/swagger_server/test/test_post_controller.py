# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.id_post_id import IdPostId  # noqa: E501
from swagger_server.models.post import Post  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPostController(BaseTestCase):
    """PostController integration test stubs"""

    def test_add_post(self):
        """Test case for add_post

        Add a new Post to the database
        """
        body = Post()
        response = self.client.open(
            '/Post',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_post(self):
        """Test case for delete_post

        Deletes Post from the database
        """
        response = self.client.open(
            '/Post',
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_post_by_id(self):
        """Test case for get_post_by_id

        Find Post by ID
        """
        response = self.client.open(
            '/Post/{Id}'.format(id=IdPostId()),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_post(self):
        """Test case for update_post

        Update an existing Post
        """
        body = Post()
        response = self.client.open(
            '/Post',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
