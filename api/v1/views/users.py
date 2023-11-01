#!/usr/bin/python3
"""view for user class"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.user import User
from flask import abort
from flask import make_response
from flask import request


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def all_users():
    """return all users"""
    dict_users = storage.all(User)
    my_users = []
    for k in dict_users.values():
        my_users.append(k.to_dict())
    return jsonify(my_users)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET'])
def get_user(user_id):
    """return user according to class"""
    if user_id:
        dict_users = storage.get(User, user_id)
        if dict_users is None:
            abort(404)
        else:
            return jsonify(dict_users.to_dict())


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """delete a user if id exists"""
    if user_id:
        users = storage.get(User, user_id)
        if users is None:
            abort(404)
        else:
            storage.delete(users)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def post_user():
    """post a user to the storage"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    re = request.get_json()
    if "email" not in re:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in re:
        return make_response(jsonify({"error": "Missing password"}), 400)
    users = User(**re)
    users.save()
    return make_response(jsonify(users.to_dict()), 201)

    @app_views.route('/users/<user_id>', strict_slashes=False,
                     methods=['PUT'])
    def update_user(user_id):
        """updates details of a user"""
        if user_id:
            users = storage.get(User, user_id)
            if users is None:
                abort(404)

            if not request.get_json():
                return make_response(jsonify({"error": "Not a JSON"}), 400)
            re = request.get_json()
            for key, value in re.items():
                if key not in ['id', 'email', 'created_at', 'updated_at']:
                    setattr(users, key, value)
            users.save()
            return make_response(jsonify(users.to_dict()), 200)
