"""
REST API Server
Emilio Coronado, emilio.mobile@gmail.com
seoulai.com
2018
"""
from flask import (Flask, request, abort, jsonify, make_response, render_template, url_for)
from flask_socketio import SocketIO, emit
from flask_httpauth import HTTPBasicAuth
import os
import random
import time as t

# Constants
BAD_REQUEST = 400
STATUS_OK = 200
NOT_FOUND = 404
SERVER_ERROR = 500
PORT = 5000

moves = [
    {
        "env_id": 123456789,
        "board_id": "0",
        "game_num": 13,
        "black": {
            "name": "random_agent",
            "pices": [
                2, 3, 4, 5, 6, 7, 9, 10, 11, 20, 30
            ],
            "win_num": 7
        },
        "white": {
            "name": "emilio",
            "pices": [
                1, 22, 23, 24, 25, 26, 27, 28, 29, 31, 32
            ],
            "win_num": 8
        }
    },
        {
            "env_id": 123456789,
            "board_id": "7",
            "game_num": 13,
            "black": {
                "name": "random_agent",
                "pices": [
                    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 20
                ],
                "win_num": 6
            },
            "white": {
                "name": "emilio",
                "pices": [
                    21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32
                ],
                "win_num": 8
            }
        },
        {
            "env_id": 123456789,
            "board_id": "0",
            "game_num": 13,
            "black": {
                "name": "random_agent",
                "pices": [
                    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
                ],
                "win_num": 6
            },
            "white": {
                "name": "emilio",
                "pices": [
                    21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32
                ],
                "win_num": 7
            }
        },
        {
            "env_id": 123456789,
            "board_id": "7",
            "game_num": 13,
            "black": {
                "name": "random_agent",
                "pices": [
                    1, 2, 3, 10, 11, 12
                ],
                "win_num": 10
            },
            "white": {
                "name": "emilio",
                "pices": [
                    21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32
                ],
                "win_num": 20
            }
        }
    ]

count = 0


def create_server(test_config=None):

    # Scoreboard Object and Data Store
    # scoreboard = Scoreboard("SEOULAI")

    # Basic Authentication
    auth = HTTPBasicAuth()

    @auth.get_password
    def get_password(username):
        if username == 'seoulAI':
            return 'agent'
        return None

    @auth.error_handler
    def unauthorized():
        return make_response(jsonify({'error': 'Unauthorized access'}), 401)

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.static_url_path='/static'

    app.config.from_mapping(
        SECRET_KEY='dev',
        #DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Now let's create the websocket
    socketio = SocketIO(app)

    @app.errorhandler(BAD_REQUEST)
    def bad_request(error):
        return make_response(jsonify({'error': 'Bad request'}), BAD_REQUEST)

    @app.errorhandler(NOT_FOUND)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), NOT_FOUND)

    # Flask Service
    @app.errorhandler(SERVER_ERROR)
    def server_error(error):
        return make_response(jsonify({'error': 'Server error'}), SERVER_ERROR)

    @app.route('/move', methods=['GET'])
    def move():
        send_move()
        return jsonify({'response': 'OK'})

    @socketio.on('message')
    def handle_message(message):
        print('received message: ' + message)

    @socketio.on('json')
    def handle_json(json):
        print('received json: ' + str(json))

    def send_move():
        # count is use to create some randomness on test moves
        global count
        count +=  1
        if (count == 4):
            count = 0
        socketio.emit('message', moves[count])

    return app