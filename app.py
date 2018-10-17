from flask import Flask, jsonify
from flask_restful import Api

from flask_jwt_extended import JWTManager

from resources.employees import EmployeeLogin, EmployeeDirectory, Employee, RegisterEmployee

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'larry'
app.config['JWT_BLACKLIST_ENABLED'] = True # allow revoked users
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh'] # allow revoked users for access and refresh tokens

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
    }),401


api.add_resource(EmployeeLogin, '/login')
api.add_resource(EmployeeDirectory, '/employees')
api.add_resource(Employee, '/employee/<string:name>')
api.add_resource(RegisterEmployee, '/employee')

app.run(port=5002, debug=True)