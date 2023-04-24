import connexion
import six

from swagger_server.models.account import Account  # noqa: E501
from swagger_server.models.id_institution_id import IdInstitutionId  # noqa: E501
from swagger_server.models.institution import Institution  # noqa: E501
from swagger_server import util


def add_institution(body):  # noqa: E501
    """Add a new Institution to the database

    Add a new Institution to the database # noqa: E501

    :param body: Create a new Institution in the database
    :type body: dict | bytes

    :rtype: Institution
    """
    if connexion.request.is_json:
        body = Institution.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_institution_by_id(id):  # noqa: E501
    """Find Institution by ID

    For valid response use only the ID structure # noqa: E501

    :param id: Id of Institution that needs to be fetched
    :type id: dict | bytes

    :rtype: Account
    """
    if connexion.request.is_json:
        id = IdInstitutionId.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_institution_by_name(name):  # noqa: E501
    """Find Institution by Name

    Find Institution by Name # noqa: E501

    :param name: Name of Institution that needs to be fetched
    :type name: str

    :rtype: Institution
    """
    return 'do some magic!'


def update_institution(body):  # noqa: E501
    """Update an existing Institution

    Update an existing Institution by Id # noqa: E501

    :param body: Update an existent Institution
    :type body: dict | bytes

    :rtype: Institution
    """
    if connexion.request.is_json:
        body = Institution.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
