#!/usr/bin/python3
"""CRUD METHDS IN THE CITY"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from models.city import City
from flask import request
from models import storage
from models.state import State
from flask import make_response


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """returns all cities of a state"""
    if state_id:
        dict_state = storage.get(State, state_id)
        if dict_state is None:
            abort(404)
        else:
            cities = storage.all(City).values()
            list_cities = []
            for city in cities:
                if city.state_id == state_id:
                    list_cities.append(city.to_dict())
            return jsonify(list_cities)


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """returns a single city
    """
    if city_id:
        dict_city = storage.get(City, city_id)
        if dict_city is None:
            abort(404)
        else:
            return jsonify(dict_city.to_dict())



@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """deletes city objs"""
    if city_id:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        else:
            storage.delete(city)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """posts a city"""
    if state_id:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    re = request.get_json()
    if "name" not in re:
        return make_response(jsonify({"error": "Missing name"}), 400)
    re['state_id'] = state_id
    city = City(**re)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=[ 'PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """updates a given city"""
    if city_id:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)

        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        re = request.get_json()
        for key, value in re.items():
            if key not in [ 'id', 'created_at', 'updated_at']:
                setattr(city, key, value)
            city.save()
            return make_response(jsonify(city.to_dict()), 200)
