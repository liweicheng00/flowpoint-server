from flask_pymongo import wrappers, PyMongo

# client = wrappers.MongoClient(
#     'mongodb://admin:sw137982@localhost:29476/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false',
#     serverSelectionTimeoutMS=20000)
# print(client)
# client.server_info()
#
# print(client.block_styles.styles)
# print(client.block_styles.styles.find_one())
# a = (client.block_styles.styles.find_one())
# print(a)
mongo = PyMongo()

# print(db)
#
# for db in client.list_databases():
#     print(db)
# import datetime

# post = {"author": "Mike",
#         "text": "My first blog post!",
#         "tags": ["mongodb", "python", "pymongo"],
#         "date": datetime.datetime.utcnow()}
#
# posts = db.posts
# post_id = posts.insert_one(post).inserted_id
#
# print(post_id)

# if __name__ == "__main__":
#     print(client)
