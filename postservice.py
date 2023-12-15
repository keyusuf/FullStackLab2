from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# In-memory data store for posts
posts = {
    '1': {'user_id': '1', 'content': 'Hello, world!'},
    '2': {'user_id': '2', 'content': 'My first blog post'}
}

@app.route('/post/<id>', methods=['GET'])
def get_post(id):
    post_info = posts.get(id, {})
    if not post_info:
        return jsonify({'error': 'Post not found'}), 404

    # Get user info from User Service
    response = requests.get(f'http://localhost:5000/user/{post_info["user_id"]}')
    if response.status_code == 200:
        post_info['user'] = response.json()

    return jsonify(post_info)

@app.route('/post', methods=['POST'])
def create_post():
    post_data = request.json
    new_id = str(max([int(k) for k in posts.keys()], default=0) + 1)
    posts[new_id] = {
        'user_id': post_data['user_id'],
        'content': post_data['content']
    }
    return jsonify(posts[new_id]), 201

@app.route('/post/<id>', methods=['PUT'])
def update_post(id):
    if id not in posts:
        return jsonify({'error': 'Post not found'}), 404
    post_data = request.json
    posts[id] = {
        'user_id': post_data['user_id'],
        'content': post_data['content']
    }
    return jsonify(posts[id])

@app.route('/post/<id>', methods=['DELETE'])
def delete_post(id):
    if id not in posts:
        return jsonify({'error': 'Post not found'}), 404
    del posts[id]
    return jsonify({'message': 'Post deleted successfully'})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
