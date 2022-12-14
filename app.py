from flask import Flask
from flask import request
from flask_mysqldb import MySQL
from flask_cors import CORS
import json
mysql = MySQL()
app = Flask(__name__)
CORS(app)
# My SQL Instance configurations
# Change these details to match your instance configurations
app.config['MYSQL_USER'] = 'Fabian'
app.config['MYSQL_PASSWORD'] = 'cloud'
app.config['MYSQL_DB'] = 'student'
app.config['MYSQL_HOST'] = '35.246.117.226'
mysql.init_app(app)


@app.route("/add")  # Add Student
def add():
    name = request.args.get('name')
    email = request.args.get('email')
    cur = mysql.connection.cursor()  # create a connection to the SQL instance
    s = '''INSERT INTO students(studentName, email) VALUES('{}','{}');'''.format(
        name, email)  # kludge - use stored proc or params
    cur.execute(s)
    mysql.connection.commit()

    return "<h1>Added user</h1>"  # Really? maybe we should check!


@app.route("/")  # Default - Show Data
def read():  # Name of the method
    cur = mysql.connection.cursor()  # create a connection to the SQL instance
    cur.execute('''SELECT * FROM students''')  # execute an SQL statment
    rv = cur.fetchall()  # Retreive all rows returend by the SQL statment
    #Results = []
    html = ""
    for row in rv:  # Format the Output Results and add to return string
        Result = {}
        Result['Name'] = row[0].replace('\n', ' ')
        Result['Email'] = row[1]
        Result['ID'] = row[2]
        #Results.append(Result)
        html = html + \
            (f"<tr style='border: 1px solid'><th >{Result['Name']}</th> <th >{Result['Email']}</th></tr> <br>")
    html = f"<table style='border: 1px solid'; width=100%; border-collapse: collapse;><tr style='border: 1px solid'><th  style='border: 1px solid'>Name</th><th style='border: 1px solid'>Email</th></tr>{html}</table>"
    return html
    #response = {'Results': Results, 'count': len(Results)}
    #ret = app.response_class(
       # response=json.dumps(response),
      #  status=200,
    #    mimetype='application/json'
    #)
   # return ret  # Return the data in a string format


@app.route("/delete")
def delete():
    name = request.args.get('name')
    cur = mysql.connection.cursor()
    str = f"DELETE from students where studentName = '{name}'"
    print(str)
    cur.execute(str)
    mysql.connection.commit()
    print("worked")
    return "<h1>Deleted user</h1>"


@app.route("/update")
def update():
    name = request.args.get('name')
    email = request.args.get('email')
    cur = mysql.connection.cursor()
    cur.execute(
        f"UPDATE students set email = '{email}' where studentName = '{name}'")
    mysql.connection.commit()
    return "<h1>Updated user</h1>"


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port='8080')  # Run the flask app at port 8080
