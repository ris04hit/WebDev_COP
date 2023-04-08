# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class IdAccountId(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, obj: str=None, uniq: str=None):  # noqa: E501
        """IdAccountId - a model defined in Swagger

        :param obj: The obj of this IdAccountId.  # noqa: E501
        :type obj: str
        :param uniq: The uniq of this IdAccountId.  # noqa: E501
        :type uniq: str
        """
        self.swagger_types = {
            'obj': str,
            'uniq': str
        }

        self.attribute_map = {
            'obj': 'obj',
            'uniq': 'uniq'
        }
        self._obj = obj
        self._uniq = uniq

    @classmethod
    def from_dict(cls, dikt) -> 'IdAccountId':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Id.Account_Id of this IdAccountId.  # noqa: E501
        :rtype: IdAccountId
        """
        return util.deserialize_model(dikt, cls)

    @property
    def obj(self) -> str:
        """Gets the obj of this IdAccountId.


        :return: The obj of this IdAccountId.
        :rtype: str
        """
        return self._obj

    @obj.setter
    def obj(self, obj: str):
        """Sets the obj of this IdAccountId.


        :param obj: The obj of this IdAccountId.
        :type obj: str
        """
        allowed_values = ["A"]  # noqa: E501
        if obj not in allowed_values:
            raise ValueError(
                "Invalid value for `obj` ({0}), must be one of {1}"
                .format(obj, allowed_values)
            )

        self._obj = obj

    @property
    def uniq(self) -> str:
        """Gets the uniq of this IdAccountId.


        :return: The uniq of this IdAccountId.
        :rtype: str
        """
        return self._uniq

    @uniq.setter
    def uniq(self, uniq: str):
        """Sets the uniq of this IdAccountId.


        :param uniq: The uniq of this IdAccountId.
        :type uniq: str
        """
        if uniq is None:
            raise ValueError("Invalid value for `uniq`, must not be `None`")  # noqa: E501

        self._uniq = uniq
