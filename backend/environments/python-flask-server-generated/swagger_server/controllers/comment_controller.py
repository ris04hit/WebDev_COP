import connexion
import six

from swagger_server.models.account import Account  # noqa: E501
from swagger_server.models.comment import Comment  # noqa: E501
from swagger_server.models.id_comment_id import IdCommentId  # noqa: E501
from swagger_server import util


def add_comment(body):  # noqa: E501
    """Add a new Comment to the database

    Add a new Comment to the database # noqa: E501

    :param body: Create a new Comment in the database
    :type body: dict | bytes

    :rtype: Comment
    """
    if connexion.request.is_json:
        body = Comment.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_comment():  # noqa: E501
    """Deletes Comment from the database

    Deletes Comment from the database # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def get_comment_by_id(id):  # noqa: E501
    """Find Comment by ID

    For valid response use only the ID structure # noqa: E501

    :param id: Id of Comment that needs to be fetched
    :type id: dict | bytes

    :rtype: Account
    """
    if connexion.request.is_json:
        id = IdCommentId.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def update_comment(body):  # noqa: E501
    """Update an existing Comment

    Update an existing Comment by Id # noqa: E501

    :param body: Update an existent Comment
    :type body: dict | bytes

    :rtype: Comment
    """
    if connexion.request.is_json:
        body = Comment.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
