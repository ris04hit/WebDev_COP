import connexion
import six

from swagger_server.models.id_post_id import IdPostId  # noqa: E501
from swagger_server.models.post import Post  # noqa: E501
from swagger_server import util


def add_post(body):  # noqa: E501
    """Add a new Post to the database

    Add a new Post to the database # noqa: E501

    :param body: Create a new Post in the database
    :type body: dict | bytes

    :rtype: Post
    """
    if connexion.request.is_json:
        body = Post.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_post():  # noqa: E501
    """Deletes Post from the database

    Deletes Post from the database # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def get_post_by_id(id):  # noqa: E501
    """Find Post by ID

    For valid response use only the ID structure # noqa: E501

    :param id: Id of Post that needs to be fetched
    :type id: dict | bytes

    :rtype: Post
    """
    if connexion.request.is_json:
        id = IdPostId.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def update_post(body):  # noqa: E501
    """Update an existing Post

    Update an existing Post by Id # noqa: E501

    :param body: Update an existent Post
    :type body: dict | bytes

    :rtype: Post
    """
    if connexion.request.is_json:
        body = Post.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
