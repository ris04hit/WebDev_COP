# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.account import Account  # noqa: E501
from swagger_server.models.comment import Comment  # noqa: E501
from swagger_server.models.id_comment_id import IdCommentId  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCommentController(BaseTestCase):
    """CommentController integration test stubs"""

    def test_add_comment(self):
        """Test case for add_comment

        Add a new Comment to the database
        """
        body = Comment()
        response = self.client.open(
            '/Comment',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_comment(self):
        """Test case for delete_comment

        Deletes Comment from the database
        """
        response = self.client.open(
            '/Comment',
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_comment_by_id(self):
        """Test case for get_comment_by_id

        Find Comment by ID
        """
        response = self.client.open(
            '/Comment/{Id}'.format(id=IdCommentId()),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_comment(self):
        """Test case for update_comment

        Update an existing Comment
        """
        body = Comment()
        response = self.client.open(
            '/Comment',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
