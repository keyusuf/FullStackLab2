from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# In-memory data store for comments
comments = {
    # Example: '1': {'user_id': '1', 'post_id': '1', 'text': 'Nice post!'}
}

@app.route('/comment/<id>', methods=['GET'])
def get_comment(id):
    comment = comments.get(id, {})
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    # Query user_service and post_service
    user_response = requests.get(f'http://localhost:5000/user/{comment["user_id"]}')
    post_response = requests.get(f'http://localhost:5001/post/{comment["post_id"]}')

    response_data = {'comment': comment}
    if user_response.status_code == 200:
        response_data['user'] = user_response.json()
    if post_response.status_code == 200:
        response_data['post'] = post_response.json()

    return jsonify(response_data)

@app.route('/comment', methods=['POST'])
def post_comment():
    comment_data = request.json
    new_id = str(max([int(k) for k in comments.keys()], default=0) + 1)
    comments[new_id] = {
        'user_id': comment_data['user_id'],
        'post_id': comment_data['post_id'],
        'text': comment_data['text']
    }
    return jsonify(comments[new_id]), 201

@app.route('/comment/<id>', methods=['PUT'])
def update_comment(id):
    if id not in comments:
        return jsonify({'error': 'Comment not found'}), 404
    comment_data = request.json
    comments[id] = {
        'user_id': comment_data['user_id'],
        'post_id': comment_data['post_id'],
        'text': comment_data['text']
    }
    return jsonify(comments[id])

@app.route('/comment/<id>', methods=['DELETE'])
def delete_comment(id):
    if id not in comments:
        return jsonify({'error': 'Comment not found'}), 404
    del comments[id]
    return jsonify({'message': 'Comment deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
