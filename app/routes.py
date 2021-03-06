# describes the process of the AI predicting a combination and outputs the score corresponding to that combo

from app import application as app, util
# from app import application as util
from flask import render_template, request
# what it was
# from codebreaker_cv import *
# what it will probably be
from agent import *
import numpy as np
import base64
import json
import os
import sys
import pickle
from calculate_score import calculate_score
from generate_random_table import *

random_score_matrix = generate_random_table()
pickle.dump(random_score_matrix, open("game_board.p", "wb"))


@app.route('/')
def index():
    return render_template('index.html', title='e-leap-ments', page='Machine Learning API')


@app.route('/test', methods=['GET'])
def test():
    data = {
        'key': 'value'
    }
    return util.success_response(200, 'This is a test response.', data)


@app.route('/play/ai', methods=['POST'])
def ai_api():
    data = request.get_json() or {}  # recieve input from the user
    playerHealth = data['playerHealth']
    aiHealth = data['aiHealth']

    print(playerHealth, aiHealth)
    # run the AI
    # os.system('python runDQN.py')
    # open the textfile saved by the AI
    f = open("action_output.txt", "r")
    # save it as a variable
    action = f.read()
    # take commas out
    action = action.replace(',', '').strip()

    # calculare the score corresponding to this action
    score = calculate_score(action, random_score_matrix)

    response = {
        'action': action,
        'score': score
    }
    f.close()
    return util.success_response(200, 'Opponent has made a move', response)
    # return util.error_response(400, 'Opponent has failed to make a move')


@app.route('/play/user', methods=['POST'])
def user_api():
    # recieve the pattern
    data = request.get_json() or {}  # recieve input from the user
    # get damage/ score
    # health_ai and health_player

    with open('actions.txt', 'w') as f:
        f.write(data["action"])
    #    f.write(",")
    #    f.write(data["action_ai"])

    random_score_matrix = pickle.load(open("game_board.p", "rb"))
    score = calculate_score(data["action"], random_score_matrix)

    response = {
        'score': score
    }
    return util.success_response(200, 'You have made a move', response)


# return util.error_response(400, 'You have failed to make a move')

if __name__ == '__main__':
    app.run()
