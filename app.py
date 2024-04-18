import pyodbc

from flask import Flask, jsonify, request

app = Flask(__name__)

server = "DESKTOP-IHH193H"
database = 'practicing'
driver = '{SQL Server}'

#server connection
try:
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};trusted_connection=Yes')
    cursor = conn.cursor()

    print("Connected to SQL server")

except pyodbc.Error as e:
    print(f'Error connecting to server: {e}')

@app.route("/")
def home():
    return "Hello world"

@app.route("/getData", methods=["GET"])
def getAuthors():
    if conn and cursor:
       try:
          cursor.execute("SELECT * FROM authors")
          list=cursor.fetchall()
          data=[]
          for i in list:
              a={"Id":i[0],"FirstName":i[1],"LastName":i[2]}
              data.append(a)
          print(data)
          return jsonify({"data":data}), 200
       except pyodbc.Error as er:
            print(f"error:{er}")
            return jsonify({"message":f"Something went wrong from getting sql:{er}"}), 500
       
    else:
        return jsonify({"message":"Please Connect database"}), 500
    

@app.route("/create_data",methods=["POST"])
def create_data():
    if conn and cursor:
       try:
          firstname=request.json.get('firstname')
          lastname=request.json.get('lastname')

          if firstname !="" and lastname !="":
              cursor.execute("INSERT INTO authors(first_name,last_name) VALUES (?,?)",(firstname,lastname))
              conn.commit()
              return jsonify({"message":"Author created Succesfully"}), 200
          else:
              return jsonify({"message":"Something went wrong"}), 500
       
       except pyodbc.Error as er:
           print(f"error:{er}")
           return jsonify({"message":f"Error in create author:{er}"}), 500
    else:
        return jsonify({"message":"Please connect database"}), 500
    
@app.route("/update_data/<int:id>",methods=["PUT"])
def update_author(id):
    if conn and cursor:
        try:
            firstname =request.json.get("firstname")
            lastname =request.json.get("lastname")

            if firstname and lastname:
                cursor.execute("UPDATE authors SET first_name=?,last_name=? WHERE id=?",(firstname,lastname,id))
                conn.commit()
                return jsonify({"message":"Updated Succesfully"}), 200
            else:
                return jsonify({"message":"Both name is required"}), 500
            
        except pyodbc.Error as er:
            print(f"error:{er}")
            return jsonify({"message":f"Something went wrong:{er}"}), 500
        
    else:
        return jsonify({"message":"Please Connect database"}), 500

@app.route("/delete_data/<int:id>", methods=["DELETE"])
def delete_author(id):
    if conn and cursor:
        try:
            cursor.execute("DELETE FROM authors WHERE id=?",(id))
            conn.commit()
            return jsonify({"message":"Deleted Sucesfully"}), 200
        except pyodbc.Error as er:
            print(f"error:{er}")
            return jsonify({"message":f"Something went wrong:{er}"}), 500
    else:
        return jsonify({"message":"Please connect database"}), 500

if __name__ == '__main__':
    app.run(host="localhost", port=5400, debug=True)