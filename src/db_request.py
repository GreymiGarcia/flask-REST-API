from flask import jsonify,request
from flask_mysqldb import MySQL

class API_db_request():
    
    def __init__(self,app):
        self.mysql = MySQL(app)

    def check_registry(self,id):
        cursor = self.mysql.connection
        cur = cursor.cursor()
        sql = "SELECT id, name, credits FROM ` courses` WHERE id = %s "
        cur.execute(sql,(id,))
        data = cur.fetchall()
        if len(data) > 0: return True
        else: return False

    def query_exec(self,id=None,method="GET"):
        try:
            cursor = self.mysql.connection
            cur = cursor.cursor()
            if id != None and method == "GET": 
                sql = "SELECT id, name, credits FROM ` courses` WHERE id = %s"
                cur.execute(sql,(id,))
                data = cur.fetchall()
            elif id != None and method == "DELETE": 
                sql = "DELETE FROM ` courses` WHERE ` courses`.`id` = %s"
                cur.execute(sql,(id,))
                cur.connection.commit()
                return jsonify({'message':"Success"})
            elif method == "GET": 
                sql = "SELECT id, name, credits FROM ` courses` ORDER BY name ASC;" 
                cur.execute(sql)
                data = cur.fetchall()
            elif method == "POST":
                sql = "INSERT INTO ` courses` (`credits`, `id`, `name`) VALUES (%s, %s, %s)"
                cur.execute(sql,(request.json['credits'],request.json['id'],request.json['name'],))
                cur.connection.commit()
                return jsonify({'message':"Success"})
            elif id != None and method == "PUT":
                sql = "UPDATE ` courses` SET `credits` = %s , `name` = %s WHERE ` courses`.`id` = %s"
                cur.execute(sql,(request.json['credits'],request.json['name'],id,))
                cur.connection.commit()
                return jsonify({'message':"Success"})
            
            if len(data) > 0: return jsonify({'courses':data,'message':'Success'})
            else: return jsonify({'message':"Course/s not found"})
        except Exception as ex:
            return jsonify({'message':"Error"})