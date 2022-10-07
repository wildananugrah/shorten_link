from flask import Flask, jsonify, request, redirect
from pymongo import MongoClient
from datetime import datetime
import json, random, string, os

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = int(os.getenv('DATABASE_PORT'))
WEB_HOST = os.getenv("WEB_HOST")

# DATABASE_HOST = "localhost"
# DATABASE_PORT = 5000
# WEB_HOST = "https://dglapm.id"

client = MongoClient(DATABASE_HOST, DATABASE_PORT)
db = client.shorten_link_db

app = Flask(__name__)

def random_str(chars = string.ascii_uppercase + string.digits, N=10):
	return ''.join(random.choice(chars) for _ in range(N))

def create_random_str():
    _random_str = random_str()
    _shorten_link = db.shorten_link.find_one(_random_str)
    if _shorten_link:
        return create_random_str()
    else:
        return _random_str

@app.route("/", methods=["GET"])
def main():
    return jsonify({ "message" : "Shorten link app is running" })

@app.route("/", methods=["POST"])
def insert_link():
    body_request = request.get_json()
    
    shorten_link = None
    if "shorten_link" in body_request:
        shorten_link = body_request['shorten_link']
    
    content = db.shorten_link.find_one({ 'shorten_link' : shorten_link })
    if content:
        return jsonify({ 'message' : 'shorten link code is not available' }), 400
    
    full_link = body_request['full_link']
    created_at = datetime.now()

    if shorten_link is None:
        shorten_link = create_random_str()

    content = {
        'shorten_link' : shorten_link,
        'full_link' : full_link,
        'created_at' : created_at
    }

    db.shorten_link.insert_one(content)
    del content['_id']

    return jsonify({
        "status" : "created",
        "data" : content
    }), 201

@app.route("/<shorten_link>")
def search_link(shorten_link):
    content = db.shorten_link.find_one({ 'shorten_link' :  shorten_link })
    if content:
        return redirect(content['full_link'])
    
    return jsonify({ "message" : f"can not find the shorten_link: {shorten_link}" }), 404


app.run(host="0.0.0.0", port=8080, debug=True)