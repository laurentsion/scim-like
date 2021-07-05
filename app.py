"""
Thales DIS - Cloud Run - SCIM like - demo
"""
import os
import requests
import google.cloud

from flask import Flask, render_template, jsonify, request

from google.cloud import firestore


# pylint: disable=C0103
app = Flask(__name__)
db = firestore.Client()
users = db.collection('users')


@app.route('/users', methods=['GET'])
def hello():
    """Return a friendly HTTP greeting."""
    message = "It's running now (users)!"
    try:
        user_id = request.args.get('id')
        if user_id:
            user = users.document(user_id).get()
            return jsonify(user.to_dict()), 200
        else:
            all_users = [doc.to_dict() for doc in users.stream()]
            return jsonify(all_users), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/users', methods=['POST'])
def add_user():
    """Return a friendly HTTP greeting."""
    message = "It's running now (users)!"

    """Get Cloud Run environment variables."""
    service = os.environ.get('K_SERVICE', 'Unknown service')
    revision = os.environ.get('K_REVISION', 'Unknown revision')

    try:
        id = request.json['id']
        users.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/users', methods=['DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection.
    """
    try:
        # Check for ID in URL query
        user_id = request.args.get('id')
        users.document(user_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
