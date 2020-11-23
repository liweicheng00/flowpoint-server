import json, os
from config import config

from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager
from flask_restful import Api

from models.model import *
from models.model_mongo import mongo


def create_app(env):
    print("ENV:", env)
    app = Flask(__name__, static_url_path='/templates', static_folder='templates', instance_relative_config=True)
    # app = Flask(__name__, instance_relative_config=True)
    if not env:
        env = 'development'
    app.config.from_object(config[env])  # from ./config.py

    register_extensions(app)

    return app


def register_extensions(app):
    db.init_app(app)
    # db = SQLAlchemy(app)
    mongo.init_app(app)

    '''REST api'''
    from resources.user import Register, Login
    from resources.styles import Styles
    from resources.files import Files

    api = Api(app)
    api.add_resource(Register, "/api/register")
    api.add_resource(Files, "/api/file")
    api.add_resource(Login, "/api/login")
    api.add_resource(Styles, "/api/styles")

    '''登入需求'''
    login_manager = LoginManager(app)

    # login_manager.login_view = 'auth.login'  # 自動導引到登入頁面

    @login_manager.user_loader  # 回傳登入物件資訊，供current_user使用
    def load_user(user):
        # user_obj = User.query.filter_by(user_id=user).first()
        # return user_obj
        return user


app = create_app("production")


@app.route('/')
def hello():
    # return render_template("dist/index.html")
    return "The demo has moved to  <a href='http://ec2-54-178-101-206.ap-northeast-1.compute.amazonaws.com/' target='_blank'>AWS server</a>"

@app.route('/db_create')
def db_create():
    db.create_all()
    return "Create all table!"


@app.route('/db_drop')
def db_drop():
    db.drop_all()
    return "Drop all table!"


@app.route('/db_q_test')
def db_q_test():
    q = User.query.all()
    result = {}
    for qq in q:
        result[qq.username] = qq.email

    return result


@app.route('/db_i_test', methods=["POST"])
def db_i_test():
    data = request.get_data()
    data = json.loads(data)
    print(data)

    for account in data:
        user = User(user_id=account['user_id'], username=account['user_id'], email=account['email'],
                    account_source=account['account_source'])
        db.session.add(user)

    db.session.commit()

    return jsonify(data)


if __name__ == "__main__":
    app = create_app("development")


    @app.route('/')
    def hello():
        # return render_template("dist/index.html")
        return "The demo has moved to  <a href='http://ec2-54-178-101-206.ap-northeast-1.compute.amazonaws.com/' target='_blank'>AWS server</a>"


    @app.route('/db_create')
    def db_create():
        db.create_all()
        return "Create all table!"


    @app.route('/db_drop')
    def db_drop():
        db.drop_all()
        return "Drop all table!"


    @app.route('/db_q_test')
    def db_q_test():
        q = User.query.all()
        result = {}
        for qq in q:
            result[qq.username] = qq.email

        return result


    @app.route('/db_i_test', methods=["POST"])
    def db_i_test():
        data = request.get_data()
        data = json.loads(data)
        print(data)

        for account in data:
            user = User(user_id=account['user_id'], username=account['user_id'], email=account['email'],
                        account_source=account['account_source'])
            db.session.add(user)

        db.session.commit()

        return jsonify(data)
    app.run(host="0.0.0.0", debug=True)
