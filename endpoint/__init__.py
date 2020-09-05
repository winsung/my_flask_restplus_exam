from flask_restplus import Api

from .user_api import api as ns_user

api = Api(
    title="nrise customer sign management",
    version="0.1",
    description="RESTful API for Customer Service using flask",
)

api.add_namespace(ns_user)