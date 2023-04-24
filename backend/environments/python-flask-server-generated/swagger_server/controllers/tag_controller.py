import connexion
import six

from swagger_server.models.account import Account  # noqa: E501
from swagger_server.models.id_tag_id import IdTagId  # noqa: E501
from swagger_server.models.tag import Tag  # noqa: E501
from swagger_server import util


def add_tag(body):  # noqa: E501
    """Add a new Tag to the database

    Add a new Tag to the database # noqa: E501

    :param body: Create a new Tag in the database
    :type body: dict | bytes

    :rtype: Tag
    """
    if connexion.request.is_json:
        body = Tag.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_tag_by_id(id):  # noqa: E501
    """Find Tag by ID

    For valid response use only the ID structure # noqa: E501

    :param id: Id of Tag that needs to be fetched
    :type id: dict | bytes

    :rtype: Account
    """
    if connexion.request.is_json:
        id = IdTagId.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_tag_by_name(name):  # noqa: E501
    """Find Tag by Name

    Find Tag by Name # noqa: E501

    :param name: Name of Tag that needs to be fetched
    :type name: str

    :rtype: Tag
    """
    return 'do some magic!'


def update_tag(body):  # noqa: E501
    """Update an existing Tag

    Update an existing Tag by Id # noqa: E501

    :param body: Update an existent Tag
    :type body: dict | bytes

    :rtype: Tag
    """
    if connexion.request.is_json:
        body = Tag.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
