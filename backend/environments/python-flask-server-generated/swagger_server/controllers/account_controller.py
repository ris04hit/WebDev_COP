import connexion
import six

from swagger_server.models.account import Account  # noqa: E501
from swagger_server import util


def add_account(body):  # noqa: E501
    """Add a new Account to the database

    Add a new Account to the database # noqa: E501

    :param body: Create a new Account in the database
    :type body: dict | bytes

    :rtype: Account
    """
    if connexion.request.is_json:
        body = Account.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_account():  # noqa: E501
    """Deletes Account from the database

    Deletes Account from the database # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def get_account_by_id(id):  # noqa: E501
    """Find Account by ID

    For valid response use only the ID structure # noqa: E501

    :param id: Id of Account that needs to be fetched
    :type id: dict | bytes

    :rtype: Account
    """
    if connexion.request.is_json:
        id = Account.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_account_by_name(username):  # noqa: E501
    """Find Account by Username

    Find Account by Username # noqa: E501

    :param username: Username of Account that needs to be fetched
    :type username: str

    :rtype: Account
    """
    return 'do some magic!'


def login_account(username=None, password=None):  # noqa: E501
    """Logs Account into the system

     # noqa: E501

    :param username: The user name for login
    :type username: str
    :param password: The password for login in clear text
    :type password: str

    :rtype: str
    """
    return 'do some magic!'


def logout_account():  # noqa: E501
    """Logs out current logged in Account session

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def update_account(body):  # noqa: E501
    """Update an existing Account

    Update an existing Account by Id # noqa: E501

    :param body: Update an existent Account
    :type body: dict | bytes

    :rtype: Account
    """
    if connexion.request.is_json:
        body = Account.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
