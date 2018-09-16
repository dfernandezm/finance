from flask import Flask
from flask import jsonify
from flask import request

import posts_mongo_repository as posts_repo

app = Flask(__name__)

@app.route('/posts', methods=['GET'])
def all_posts():
    posts_repo.connect()
    all_posts = posts_repo.find_all_posts()
    return jsonify({'posts' : all_posts})


@app.route('/post', methods=['POST'])
def add_post():
    post_payload = request.json['post']
    posts_repo.insert_post(db,post_payload)
    #return jsonify({'result' : output})
    return ('', 204)


if __name__ == '__main__':
   app.run(debug=True)