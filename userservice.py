from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data store for users
users = {
    '1': {'name': 'Alice', 'email': 'alice@example.com'},
    '2': {'name': 'Bob', 'email': 'bob@example.com'}
}

@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user_info = users.get(id, {})
    if not user_info:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user_info)

@app.route('/user', methods=['POST'])
def create_user():
    user_data = request.json
    new_id = str(max([int(k) for k in users.keys()]) + 1)  # generate new id
    users[new_id] = user_data
    return jsonify(users[new_id]), 201

@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    if id not in users:
        return jsonify({'error': 'User not found'}), 404
    user_data = request.json
    users[id] = user_data
    return jsonify(users[id])

@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    if id not in users:
        return jsonify({'error': 'User not found'}), 404
    del users[id]
    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
