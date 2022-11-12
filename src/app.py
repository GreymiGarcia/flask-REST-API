from flask import Flask,jsonify,request
from config import config
from flask_mysqldb import MySQL

app = Flask(__name__)

mysql = MySQL(app)

def check_registry(id):
    cursor = mysql.connection
    cur = cursor.cursor()
    sql = "SELECT id, name, credits FROM ` courses` WHERE id = '{0}'".format(id) 
    cur.execute(sql)
    data = cur.fetchall()
    if len(data) > 0: return True
    else: return False

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
        elif id != None and method == "PUT":
            sql = """UPDATE ` courses` SET `credits` = '{0}', `name` = '{1}' WHERE ` courses`.`id` = {2};
            """.format(request.json['credits'],request.json['name'],id)
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
    if check_registry(format(request.json['id'])) == False: return get_query(method="POST")
    else: return jsonify({'message':"ID already exists"})

@app.route('/<id>', methods=['GET'])
def get_course(id):
    return get_query(id)

@app.route('/<id>', methods=['DELETE'])
def del_course(id):
    if check_registry(id) == True: return get_query(id,method="DELETE")
    else: return jsonify({'message':"ID do not exists"})

@app.route('/<id>', methods=['PUT'])
def update_course(id):
    if check_registry(id) == True: return get_query(id,method="PUT")
    else: return jsonify({'message':"ID do not exists"})

def not_found(error):
    return "<h1>Page not found!</h1>"

if __name__=="__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404,not_found)
    app.run()