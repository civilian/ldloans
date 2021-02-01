from flask import Blueprint, request, make_response, jsonify

from project.server import bcrypt, db
from project.server.models import User

def handle_request_with_authorisation_token(func):
    """Decorator to handle all that needs to happen with the autorization token"""
    def _handle_request_with_authorisation_token(*args, **kwargs):
        # get the auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                return func(user=user, *args, **kwargs)
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401
    
    return _handle_request_with_authorisation_token