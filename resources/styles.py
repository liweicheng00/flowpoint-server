from pprint import pprint

from flask_restful import Resource

from models.model_mongo import mongo
from bson.json_util import dumps, CANONICAL_JSON_OPTIONS, RELAXED_JSON_OPTIONS, loads
import json


class Styles(Resource):
    # parser = reqparse.RequestParser()
    # parser.add_argument('user_id', required=True, help='ID is required')
    # parser.add_argument('username', required=True, help='name is required')
    # parser.add_argument('email', required=True, help='pwd_confirm is required')
    # parser.add_argument('account_source', required=True, help='pwd_confirm is required')
    # parser.add_argument('pwd', required=True, help='pwd is required')
    # parser.add_argument('pwd_confirm', required=True, help='pwd_confirm is required')
    # parser.add_argument('old_pwd', required=False, help='pwd_confirm is required')

    def get(self):
        a = dumps((mongo.db.styles.find()), json_options=RELAXED_JSON_OPTIONS)
        return json.loads(a)

    def post(self):
        # arg = self.parser.parse_args()
        pass

    def put(self):
        # arg = self.parser.parse_args()
        pass

    def delete(self):
        pass
