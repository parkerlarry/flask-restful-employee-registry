from flask_restful import Resource, reqparse

from werkzeug.security import safe_str_cmp

from flask_jwt_extended import (jwt_required,
                                create_access_token,
                                create_refresh_token,
                                get_jwt_identity,
                                jwt_refresh_token_required)

from models.credentials import Credentials

from models.employees import Employees

import uuid  # each employee gets a unique id

_employee_db = 'database/employees.json'  # filename to use for employee database

_credentials_db = 'database/credentials.json'  # filename to use for credentials database

_employees = Employees(_employee_db)  # create new instance of employees registry

_credentials = Credentials(_credentials_db)  # create new instance of credentials registry

_user_parser = reqparse.RequestParser()  # allow parser to handle parameters

_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="Username can not be left blank"
                          )

_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="Password can not be left blank"
                          )

_employee_parser = reqparse.RequestParser()

_employee_parser.add_argument('employee_type',
                              type=str,
                              required=True,
                              help="employee_type can not be left blank"
                              )

_employee_parser.add_argument('user_name',
                              type=str,
                              required=True,
                              help="user_name can not be left blank"
                              )

_employee_parser.add_argument('real_name',
                              type=str,
                              required=True,
                              help="real_name can not be left blank"
                              )

_employee_parser.add_argument('phone_number',
                              type=str,
                              required=True,
                              help="phone_number can not be left blank"
                              )

_member_parser = reqparse.RequestParser()

_member_parser.add_argument('employee_type',
                            type=str,
                            required=True,
                            help="employee_type can not be left blank"
                            )

_member_parser.add_argument('user_name',
                            type=str,
                            required=True,
                            help="user_name can not be left blank"
                            )

_member_parser.add_argument('real_name',
                            type=str,
                            required=True,
                            help="real_name can not be left blank"
                            )

_member_parser.add_argument('phone_number',
                            type=str,
                            required=True,
                            help="phone_number can not be left blank"
                            )

_member_parser.add_argument('password',
                            type=str,
                            required=True,
                            help="password can not be left blank"
                            )


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200


class EmployeeLogin(Resource):

    @classmethod
    def post(cls):
        # get data from parser
        request_data = _user_parser.parse_args()

        # find user in database
        user = _credentials.find_by_username(request_data['username'])

        # return tokens
        if user and safe_str_cmp(user['password'], request_data['password']):
            access_token = create_access_token(identity=user['user_id'], fresh=True)
            refresh_token = create_refresh_token(identity=user['user_id'])

            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200

        return {'message': 'Invalid credentials'}, 401

        # FIXME: find out if token is stolen, can attacker know which endpoint to use the token on?


class EmployeeDirectory(Resource):
    @jwt_required
    def get(self):
        employees = _employees.get_employees()

        # access cant be granted to someone who is not in the system
        if len(employees) == 0:
            return {'message': 'Access denied'}, 401

        # find the identity of the person calling this function
        identity = get_jwt_identity()

        username = _credentials.find_by_userid(identity)

        if username is None:
            return {'message': 'Access denied'}, 401

        username = username['user_name']

        user = _employees.find_by_username(username)

        if user['employee_type'] == 'manager':
            return {'Employees': _employees.get_employees()}, 200

        return {'message': 'Access denied. Admin privilege required'}, 401


class RegisterEmployee(Resource):
    def post(self):
        request_data = _employee_parser.parse_args()

        employee_type = request_data['employee_type']

        if employee_type != 'manager' and employee_type != 'regular':
            return {'message': "employee_type can not be '{}'".format(employee_type)}, 400

        user_name = request_data['user_name']

        employee = _employees.find_by_username(user_name)

        if employee is None:
            _employees.update_employees(_employee_db, request_data, 'add')

            new_user = {
                "user_name": user_name,
                "password": "#changeme123!",
                "user_id": uuid.uuid4().int
            }

            _credentials.update_credentials(_credentials_db, new_user, 'add')

            return {"new_employee": request_data}, 201

        return {'message': "Employee with user_name '{}' already exists".format(user_name)}, 400


class Employee(Resource):
    @jwt_required
    def get(self, name):

        employee = _employees.find_by_username(name)

        if employee is None:
            # FIXME: Username discovery should not be allowed

            # return {'message': "User '{}' not found".format(name)}, 404

            # FIXED :

            return {'message': "Access denied!"}, 404

        # find the identity of the user calling this function

        identity = get_jwt_identity()

        username = _credentials.find_by_userid(identity)

        if username is None:
            return {'message': 'Access denied!'}, 401

        else:
            username = username['user_name']

        user = _employees.find_by_username(username)

        if user is None:  # if user not found

            return {'message': 'Access denied. Invalid credentials'}, 401

        elif user['employee_type'] == 'manager' or user['user_name'] == name:
            return {'Employee': employee}, 200

    @jwt_required
    def put(self, name):

        employee = _employees.find_by_username(name)

        if employee is None:
            # FIXME: Username discovery should not be allowed

            # return {'message': "User '{}' not found".format(name)}, 404

            # FIXED :

            return {'message': " "}, 404

        # find the identity of the user calling this function
        identity = get_jwt_identity()

        username = _credentials.find_by_userid(identity)['user_name']
        user = _employees.find_by_username(username)

        if user is None:
            return {'message': 'Access denied. Invalid credentials'}, 401

        elif user['user_name'] == name:

            request_data = _member_parser.parse_args()

            new_employee = {
                "employee_type": request_data['employee_type'],
                "user_name": request_data['user_name'],
                "real_name": request_data['real_name'],
                "phone_number": request_data['phone_number']
            }

            new_user = {
                "user_name": request_data['user_name'],
                "password": request_data['password'],
                "user_id": identity
            }

            _employees.update_employees(_employee_db, new_employee, 'update')

            _credentials.update_credentials(_credentials_db, new_user, 'update')

            # TODO: send a new token
            return {'Employee': new_employee}, 200

        else:
            return {'message': 'Access denied. Admin privilege required!'}, 401

    @jwt_required
    def delete(self, name):

        old_employee = _employees.find_by_username(name)

        old_user = _credentials.find_by_username(name)

        if old_employee is None:
            # FIXME: Username discovery should not be allowed

            # return {'message': "User '{}' not found".format(name)}, 404

            # FIXED :

            return {'message': " "}, 404

        # find the identity of the user calling this function

        identity = get_jwt_identity()

        username = _credentials.find_by_userid(identity)['user_name']

        user = _employees.find_by_username(username)

        if user is None:

            return {'message': 'Access denied. Invalid credentials'}, 401

        elif user['employee_type'] == 'manager' or user['user_name'] == name:

            _employees.update_employees(_employee_db, old_employee, 'delete')

            _credentials.update_credentials(_credentials_db, old_user, 'delete')

            # TODO: revoke old token

            return {'message': "employee deleted"}, 200

        else:
            return {'message': 'Access denied. Admin privilege required!'}, 401
