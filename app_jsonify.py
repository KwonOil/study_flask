from flask import Flask, request, jsonify

app = Flask(__name__)
user_data = {}

@app.route('/user/<username>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_user(username=None):
    if request.method == 'GET':
        return jsonify({username : user_data.get(username, 'Not found')})
    
    elif request.method == 'POST':
        new_data = request.json
        user_data[username] = new_data
        return jsonify(user_data), 201
    
    elif request.method == 'PUT':
        update_data = request.json
        if username in user_data:
            user_data[username].update(update_data)
            return jsonify(update_data)
        else:
            return jsonify({'error': 'User not found'}), 404
        
    elif request.method == 'DELETE':
        if username in user_data:
            del user_data[username]
            return jsonify({"reusult": "User deleted"}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
