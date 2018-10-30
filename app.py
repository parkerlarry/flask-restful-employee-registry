from flask import Flask, jsonify

from flask_restful import Api

from flask_jwt_extended import JWTManager

from resources.employees import EmployeeLogin, EmployeeDirectory, Employee, RegisterEmployee, TokenRefresh

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'larry'

app.config['JWT_BLACKLIST_ENABLED'] = True  # allow revocation of users / blacklisting

app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # enable blacklisting of access and refresh tokens

blacklist = [0, 1, 2]  # TODO: This is an example, but these user ids will be blacklisted.

api = Api(app)

jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def deny_access(decoded_token):  # returns true if token is blacklisted
    return decoded_token['identity'] in blacklist


@jwt.revoked_token_loader  # use case: a user that has been logged out, gets his/her token revoked
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401


@jwt.expired_token_loader  # callback for when token has expired after 5 mins
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired. Please refresh! ',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader  # callback for when a non-jwt token string is entered in the header field
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader  # callback for when token is not provided
def missing_token_callback(error):
    return jsonify({
        'description': ' Request is missing a token.',
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader  # callback for when token is not fresh
def missing_token_callback():
    return jsonify({
        'description': ' Request is missing a fresh token.',
        'error': 'fresh_token_required'
    }), 401


api.add_resource(EmployeeLogin, '/login')  # login endpoint for handling existing (registered) employees

api.add_resource(EmployeeDirectory, '/employees')  # employee resource endpoint for all employees

api.add_resource(Employee, '/employee/<string:name>')  # employee resource endpoint for single employee

api.add_resource(RegisterEmployee, '/employee')  # employee resource endpoint for handling new employees

api.add_resource(TokenRefresh, '/refresh')

#app.run(port=5000, debug=True)
