import datetime
import json

from bson.json_util import dumps, RELAXED_JSON_OPTIONS
from bson.objectid import ObjectId
from flask_restful import Resource, reqparse

from models.model import db, File as File_model
from models.model_mongo import mongo


class Files(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('file_id', required=False, help='file_id is required', action="append")
    parser.add_argument('user_id', required=False, help='user_id is required')
    parser.add_argument('file_name', required=False, help='file_name is required')
    parser.add_argument('data', required=False, help='data is required', type=dict)
    parser.add_argument('styles', required=False, help='styles is required', action="append")

    def get(self):
        # get demo file
        q = File_model.query.filter_by(user_id='demo1').all()
        ids = []
        for qq in q:
            ids.append(ObjectId(qq.file_id))

        files = mongo.db.files

        a = dumps(files.find({"_id": {"$in": ids}}), json_options=RELAXED_JSON_OPTIONS)
        return json.loads(a)

    def post(self):
        # 1. check is allowed to get files
        # 2. get files from MongoDB files
        # 3. get styles from MongoDB styles
        arg = self.parser.parse_args()

        is_allowed = File_model.query.filter(File_model.file_id.in_(arg.file_id),
                                             File_model.user_id == arg.user_id).first()
        if is_allowed:
            files = mongo.db.files
            result = files.find_one({"_id": ObjectId(is_allowed.file_id)})
            data = dumps(result, json_options=RELAXED_JSON_OPTIONS)

            styles = mongo.db.styles

            s = styles.find({"name": {"$in": result['styles']}})
            style = (dumps(s, json_options=RELAXED_JSON_OPTIONS))

            return {"data": json.loads(data), "styles": json.loads(style)}
        else:
            msg = "You are not the allowed!"
            return msg, 400

    def put(self):
        # save files
        arg = self.parser.parse_args()
        files = mongo.db.files

        is_file = File_model.query.filter(File_model.user_id == arg.user_id,
                                          File_model.file_id.in_(arg.file_id)).first()
        if is_file:
            is_file.update_date = datetime.datetime.now()
            db.session.add(is_file)
            db.session.commit()

            try:
                # file_id = files.insert_one(save_file).inserted_id
                result = files.replace_one({'_id': ObjectId(arg.file_ud)}, {
                    '$set': {"data": arg.data, "styles": arg.styles, "file_name": arg.file_name}})
            except Exception as e:
                return "update file fail! {} {}".format(arg.file_name, str(e)), 400
            else:
                return {"msg": "Update file: {}, _id: {}".format(",".join(arg.file_name), arg.file_id)}

        else:

            save_file = {
                "file_name": arg.file_name,
                "data": arg.data,
                "styles": arg.styles
            }
            print(arg.file_name)
            try:
                file_id = files.insert_one(save_file).inserted_id
                f = File_model(user_id=arg.user_id, file_id=str(file_id), file_name=arg.file_name,
                               created_date=datetime.datetime.now(), update_date=datetime.datetime.now())
                db.session.add(f)
                db.session.commit()
            except Exception as e:
                return "Saving file fail! {} {}".format(",".join(arg.file_name), str(e)), 400
            else:
                return {"msg": "Saved file: {}, _id: {}".format(arg.file_name, file_id), "file_id": str(file_id)}

    def delete(self):
        # delete files
        arg = self.parser.parse_args()
        # files = mongo.db.files
        q = File_model.query.filter(File_model.file_id.in_(arg.file_id)).all()
        for qq in q:
            qq.delete_flag = True
            qq.delete_data = datetime.datetime.now()
            db.session.add(qq)

        try:
            db.session.commit()
        except Exception as e:
            return "Delete file fail! {}".format(str(e))
        else:
            return "delete file: {}".format(", ".join(arg.file_name))

    # try:
    #     result = files.delete_many({"_id": {"$in": [ObjectId(file_id) for file_id in arg.file_id]}})
    # except Exception as e:
    #     return "Delete file fail! {}".format(str(e))
    #
    # if result.deleted_count != 0:
    #     return "delete file: {}".format(", ".join(arg.file_name))
    # else:
    #     return {"msg": "Can not delete file: {}".format(", ".join(arg.file_name))}, 400
