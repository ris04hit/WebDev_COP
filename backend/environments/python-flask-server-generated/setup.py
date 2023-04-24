# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "swagger_server"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion",
    "swagger-ui-bundle>=0.0.2"
]

setup(
    name=NAME,
    version=VERSION,
    description="Synergy API",
    author_email="cs1210547@iitd.ac.in",
    url="",
    keywords=["Swagger", "Synergy API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['swagger_server=swagger_server.__main__:main']},
    long_description="""\
    A collaborative space for people who want to share their knowledge and resource. Whether need to share in an organization or publically to all or only to friends, Synergy is here. Anybody with need of getting some resources, just search it and surely somebody will be there who has posted the related content for you. This is a swagger documentation which provides API for Synergy website.
    """
)
