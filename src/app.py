from flask import Flask,jsonify,request
from config import config
from flask_mysqldb import MySQL

app = Flask(__name__)

mysql = MySQL(app)

def get_query(id=None,method="GET"):
    try:
        cursor = mysql.connection
        cur = cursor.cursor()
        if id != None and method == "GET": 
            sql = "SELECT id, name, credits FROM ` courses` WHERE id = '{0}'".format(id) 
            cur.execute(sql)
            data = cur.fetchall()
        elif id != None and method == "DELETE": 
            sql = "DELETE FROM ` courses` WHERE ` courses`.`id` = {0};".format(id) 
            cur.execute(sql)
            cur.connection.commit()
            return jsonify({'message':"Success"})
        elif method == "GET": 
            sql = "SELECT id, name, credits FROM ` courses` ORDER BY name ASC;" 
            cur.execute(sql)
            data = cur.fetchall()
        elif method == "POST":
            sql = """INSERT INTO ` courses` (`credits`, `id`, `name`) 
            VALUES ({0},{1},'{2}');""".format(request.json['credits'],request.json['id'],request.json['name'])
            cur.execute(sql)
            cur.connection.commit()
            return jsonify({'message':"Success"})
        
        if len(data) > 0: return jsonify({'courses':data,'message':'Success'})
        else: return jsonify({'message':"Course/s not found"})
    except Exception as ex:
        return jsonify({'message':"Error"})

@app.route('/', methods=['GET'])
def index():
    return get_query()

@app.route('/', methods=['POST'])
def set_course():
    return get_query(method="POST")

@app.route('/<id>', methods=['GET'])
def get_course(id):
    return get_query(id)

@app.route('/<id>', methods=['DELETE'])
def del_course(id):
    return get_query(id,method="DELETE")

def not_found(error):
    return "<h1>Page not found!</h1>"

if __name__=="__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404,not_found)
    app.run()