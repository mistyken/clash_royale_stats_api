import os
import boto3
from flask import Flask, jsonify, request

app = Flask(__name__)

PLAYERS_TABLE = os.environ['PLAYERS_TABLE']
IS_OFFLINE = os.environ.get('IS_OFFLINE')

if IS_OFFLINE:
    client = boto3.client(
        'dynamodb',
        region_name='localhost',
        endpoint_url='http://localhost:8000'
    )
else:
    client = boto3.client('dynamodb')
    

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/players/<string:player_id>")
def get_player(player_id):
    resp = client.get_item(
        TableName=PLAYERS_TABLE,
        Key={
            'playerId': { 'S': player_id }
        }
    )
    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'Player does not exist'}), 404

    return jsonify({
        'playerId': item.get('playerId').get('S'),
        'name': item.get('name').get('S')
    })


@app.route("/players", methods=["POST"])
def create_player():
    player_id = request.json.get('playerId')
    name = request.json.get('name')
    if not player_id or not name:
        return jsonify({'error': 'Please provide playerId and name'}), 400

    resp = client.put_item(
        TableName=PLAYERS_TABLE,
        Item={
            'playerId': {'S': player_id },
            'name': {'S': name }
        }
    )

    return jsonify({
        'playerId': player_id,
        'name': name
    })