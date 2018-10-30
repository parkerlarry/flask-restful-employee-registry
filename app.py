from flask import Flask, jsonify

from flask_restful import Api

from flask_jwt_extended import JWTManager

from resources.employees import EmployeeLogin, EmployeeDirectory, Employee, RegisterEmployee

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'larry'

app.config['JWT_BLACKLIST_ENABLED'] = True  # allow revocation of users

app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow token based user access and token expiration

api = Api(app)

jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def deny_access(decoded_token):
    return decoded_token['identity'] in [0]


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401


api.add_resource(EmployeeLogin, '/login')  # login endpoint for handling existing (registered) employees

api.add_resource(EmployeeDirectory, '/employees')  # employee resource endpoint for all employees

api.add_resource(Employee, '/employee/<string:name>')  # employee resource endpoint for single employee

api.add_resource(RegisterEmployee, '/employee')  # employee resource endpoint for handling new employees

# app.run(port=5000, debug=True)
