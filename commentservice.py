from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# In-memory data store for comments
comments = {
    # Example: "1": {"comment_id": 1, "user_id": 1, "post_id": 1, "text": "Sample comment"}
}

# Assuming user_service and post_service have URLs like "http://user_service" and "http://post_service"
USER_SERVICE_URL = "http://user_service"
POST_SERVICE_URL = "http://post_service"

@app.route('/comment/<int:id>', methods=['GET'])
def get_comment(id):
    comment = comments.get(str(id))
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    # Query user_service and post_service
    user_response = requests.get(f"{USER_SERVICE_URL}/user/{comment['user_id']}")
    post_response = requests.get(f"{POST_SERVICE_URL}/post/{comment['post_id']}")

    if user_response.status_code != 200 or post_response.status_code != 200:
        return jsonify({'error': 'Unable to fetch user or post information'}), 500

    user_info = user_response.json()
    post_info = post_response.json()

    # Combine data
    combined_data = {
        "comment": comment,
        "user": user_info,
        "post": post_info
    }

    return jsonify(combined_data)

@app.route('/comment', methods=['POST'])
def post_comment():
    # Example of creating a new comment
    comment_data = request.json
    new_id = str(len(comments) + 1)
    comments[new_id] = {
        "comment_id": new_id,
        "user_id": comment_data["user_id"],
        "post_id": comment_data["post_id"],
        "text": comment_data["text"]
    }
    return jsonify(comments[new_id]), 201

if __name__ == '__main__':
    app.run(debug=True)
