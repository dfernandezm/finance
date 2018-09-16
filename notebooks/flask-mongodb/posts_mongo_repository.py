from pymongo import MongoClient

# docker run --name some-mongo -v /path/to/mongodb/data/db:/data/db -p 27017:27017 -it mongo
db = None

def connect():
    global db
    (client, db) = _connect_to_mongo('mongodb://localhost:27017/','restdb')


def _connect_to_mongo(mongo_url, dbname):
    client = MongoClient(mongo_url)
    db = client[dbname]
    return (client, db)


def delete_all_posts(db):
    db.posts.drop()


def id_to_str(post):
    for k,v in post.items():
        if k == "_id":
            post['_id'] = str(post['_id'])
            return post


def find_all_posts():
    posts = db.posts.find()
    all_posts = [ id_to_str(p) for p in posts ]
    return all_posts


def print_posts(posts):
    all_posts = [ p for post in posts ]
    print(all_posts)


def insert_post(db, post):
    post_id = db.posts.insert_one(post)

    return post_id.inserted_id

def insert_posts(db, posts_list):
    ins_ids = db.posts.insert_many(posts_list).inserted_ids
    return list(map(lambda _id: str(_id), ins_ids))


def list_collection_names(db):
    print(db.list_collection_names())


def detail_python_object(_object):
    pass
    # only for Jupyter
    # _object??