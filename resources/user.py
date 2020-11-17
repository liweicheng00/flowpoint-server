# from flask_principal import identity_changed, AnonymousIdentity, Identity
from pprint import pprint

from flask import (
    current_app, jsonify
)
from flask_login import login_user, current_user
from flask_restful import Resource, reqparse
from google.auth.transport import requests
from google.oauth2 import id_token
from werkzeug.security import check_password_hash, generate_password_hash

from models.model import db, User as User_model, File

class Register(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', required=True, help='ID is required')
    parser.add_argument('username', required=True, help='name is required')
    parser.add_argument('email', required=True, help='pwd_confirm is required')
    parser.add_argument('account_source', required=True, help='pwd_confirm is required')
    parser.add_argument('pwd', required=True, help='pwd is required')
    parser.add_argument('pwd_confirm', required=True, help='pwd_confirm is required')
    parser.add_argument('old_pwd', required=False, help='pwd_confirm is required')

    def get(self, name):
        print('user get')
        return [name]

    def post(self):
        arg = self.parser.parse_args()
        msg = None
        if not arg['pwd'] == arg['pwd_confirm']:
            msg = 'Password is not the same.'
        elif User_model.query.filter_by(username=arg['ID']).first() is not None:
            msg = 'user_name {} is already registered.'.format(arg['ID'])

        if msg is None:
            new_client = User_model(username=arg['ID'], password=generate_password_hash(arg['pwd']), name=arg['name'])
            db.add(new_client)
            db.commit()
            msg = 'register success'
            return {"msg": msg}

        return {
            "msg": msg
        }

    def put(self):
        arg = self.parser.parse_args()
        user = User_model.query.filter_by(username=arg['ID']).first()
        if user is not None:
            if check_password_hash(user.password, arg.old_pwd):
                if arg['pwd'] == arg['pwd_confirm']:
                    user.password = generate_password_hash(arg['pwd'])
                    db.add(user)
                    db.commit()
                    msg = 'revise success'
                else:
                    msg = "password not match."
            else:
                msg = 'Incorrect password.'

        else:
            msg = "no this user"
        return {
            'msg': msg
        }

    def delete(self):
        pass


class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', required=False, help='ID is required')
    parser.add_argument('login_type', required=True, help='login_type is required')
    parser.add_argument('token', required=False, help='token is required')

    parser.add_argument('email', required=False, help='ID is required')
    parser.add_argument('account_source', required=False, help='ID is required')
    parser.add_argument('username', required=False, help='ID is required')
    parser.add_argument('pwd', required=False, help='pwd is required')

    def get(self):
        if current_user.is_anonymous:
            return {
                "msg": "not login",
                "user": None
            }
        else:
            user = current_user.username
            name = current_user.name
            return {
                "user": {
                    "username": user,
                    "name": name
                }
            }

    def post(self):
        arg = self.parser.parse_args()
        msg = None
        if arg.login_type == 'google':
            try:
                # Specify the CLIENT_ID of the app that accesses the backend:
                idinfo = id_token.verify_oauth2_token(arg.token, requests.Request(), current_app.config['CLIENT_ID'])
                # Or, if multiple clients access the backend server:
                # idinfo = id_token.verify_oauth2_token(token, requests.Request())
                # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
                #     raise ValueError('Could not verify audience.')

                # If auth request is from a G Suite domain:
                # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
                #     raise ValueError('Wrong hosted domain.')

                # ID token is valid. Get the user's Google Account ID from the decoded token.
                user_id = idinfo['sub']

            except ValueError:
                # Invalid token
                msg = "Invalid token"
                return msg
            user = User_model.query.filter_by(user_id=user_id, account_source=arg.login_type).first()
            if user:
                login_user(user)
                # getFiles
                files = File.query.filter_by(user_id=user_id).order_by(File.update_date.desc()).all()
                files_name = []
                for f in files:
                    files_name.append(f.file_name)
                return {"username": user.username, "user_id": user.user_id, "files_name": files_name}

            else:
                try:
                    user = User_model(user_id=idinfo['sub'],
                                      username=idinfo['name'],
                                      email=idinfo['email'],
                                      account_source=arg.login_type)
                    db.session.add(user)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    msg = "Register account failed!"
                    return msg
                login_user(user)
                return {"username": user.username, "user_id": user.user_id, "files_name": []}

        else:

            # user = User_model.query.filter_by(user_id=arg.user_id).first()
            # if not user:
            #     #     create account
            #     try:
            #         user = User_model(user_id=arg.user_id,
            #                           username=arg.username,
            #                           email=arg.email,
            #                           account_source=arg.account_source)
            #         db.session.add(user)
            #         db.session.commit()
            #     except Exception as e:
            #         print(e)
            #         return e
            #     else:
            #         msg = "New account!"
            #
            # login_user(user)
            # print("logged")
            # return jsonify({"msg": msg,
            #                 "user": {
            #                     "user_id": user.user_id,
            #                     "username": user.username,
            #                     "email": user.email,
            #                     "account_source": user.account_source
            #                 }})
            msg = "Use google for login"
            return msg

#
#
# error = None
# if user is None:
#     error = 'ID is not exist.'
#
# #     create account
#
#
# elif not check_password_hash(user.password, arg.pwd):
#     error = 'Incorrect password.'
#
# if error is None:
#     identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
#     login_user(user)
#     return {"msg": error,
#             "user": {
#                 "username": user.username,
#                 "name": user.name
#             }}
# return {
#     "msg": error,
#     "user": None
# }

def put(self, name):
    pass

# def delete(self):
#     logout_user()
#     for key in ('identity.name', 'identity.auth_type'):
#         session.pop(key, None)
#     identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
#     return {"msg": "logout!"}
