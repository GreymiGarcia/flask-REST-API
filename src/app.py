from flask import Flask,jsonify,request
from flask_cors import CORS
from config import config
import db_request

app = Flask(__name__)

CORS(app,resources={r"/*":{"origin":"http://localhost"}})

req = db_request.API_db_request(app)

@app.route('/', methods=['GET'])
def index():
    return req.query_exec()

@app.route('/', methods=['POST'])
def set_course():
    if req.check_registry(format(request.json['id'])) == False: return req.query_exec(method="POST")
    else: return jsonify({'message':"ID already exists"})

@app.route('/<id>', methods=['GET'])
def get_course(id):
    return req.query_exec(id)

@app.route('/<id>', methods=['DELETE'])
def del_course(id):
    if req.check_registry(id) == True: return req.query_exec(id,method="DELETE")
    else: return jsonify({'message':"ID do not exists"})

@app.route('/<id>', methods=['PUT'])
def update_course(id):
    if req.check_registry(id) == True: return req.query_exec(id,method="PUT")
    else: return jsonify({'message':"ID do not exists"})

def not_found(error):
    return "<h1>Page not found!</h1>"

if __name__=="__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404,not_found)
    app.run()