from flask import Flask,jsonify
from config import config
from flask_mysqldb import MySQL

app = Flask(__name__)

mysql = MySQL(app)

@app.route('/', methods=['GET'])
def index():
    try:
        cursor = mysql.connection
        cur = cursor.cursor()
        sql = "SELECT id, name, credits FROM ` courses` ORDER BY name ASC;"
        cur.execute(sql)
        data = cur.fetchall()
        return jsonify({'courses':data,'message':"successs"})
    except Exception as ex:
        return jsonify({'message':"Error"})

def not_found(error):
    return "<h1>Page not found!</h1>"

if __name__=="__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404,not_found)
    app.run()