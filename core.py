import MySQLdb.cursors
from flask import Flask, request, url_for, render_template, json, abort, flash,jsonify
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from passlib.hash import pbkdf2_sha256
import re
load_dotenv()
import os
from database import dbuser

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'kasir'
 
mysql = MySQL(app)

# coba disini
@app.route('/check')
def access():
    cur = dbuser.conn
    cursor = cur.connection.cursor()
    cursor.execute("SELECT * FROM user")
    data = cursor.fetchall()
    return jsonify()

# coba selesai
@app.route('/user')
def user():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user")
    resultset = cursor.fetchall()
    return jsonify(resultset)


@app.route('/user/create', methods=['POST'])
def usercreate():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        user_pass = request.form['user_pass']
        level = request.form['level']
        nationality_id = request.form['nationality_id']
        address = request.form['address']
        phone = request.form['phone']
        userpass = request.form['userpass']
        userhash = pbkdf2_sha256.hash(userpass)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        account = cursor.fetchone()
        if account :
            message = 'account already exist'
        elif not re.match(r'[^@]+@[^@]+\.[^@]', email):
            message = 'invalid email address'
        elif userpass != user_pass:
            message = 'your verification password is false'
        else :
            que = """
            INSERT INTO user (name, email,user_pass, level, nationality_id, address, phone) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            value = (name, email, userhash, level, nationality_id, address, phone,)
            cursor.execute(que, value)
            mysql.connection.commit()
            cursor.close()
            message = 'you have succesfully registered!'
    else:
        message = 'gagal'
    return message

@app.route('/user/put/<user_id>', methods=['GET', 'POST'])
def edit(user_id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM user WHERE user_id = %s", (user_id,))
        resultset = cursor.fetchone()
        return jsonify(
            user_id = resultset[0],
            nama = resultset[1],
            email = resultset[2],
            user_pass = resultset[3],
            level = resultset[4],
            nationality_id = resultset[5],
            address = resultset[6],
            phone = resultset[7]
        )
    else :
        user_id = request.form['user_id']
        email = request.form['email']
        name = request.form['name']
        user_pass = request.form['user_pass']
        level = request.form['level']
        nationality_id = request.form['nationality_id']
        address = request.form['address']
        phone = request.form['phone']

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE user SET name = %s, email = %s, user_pass = %s, nationality_id = %s, address = %s, phone = %s WHERE user_id = %s", (name, email, user_pass, nationality_id, address,phone, level, user_id, ))
        action = mysql.connection.commit()
        return jsonify(action)


        # cursor = mysql.connection.cursor()
        # cursor.execute("UPDATE user SET nama = ")

# @app.route("/user/edit", methods='PUT')
# def editpost():
#     cursor = mysql.connection.cursor()
#     request.get_json()
#     cursor.execute("UPDATE user SET email = ")


        
        
        

