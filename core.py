import MySQLdb.cursors
from flask import Flask, request, url_for, render_template, json, abort, flash,jsonify
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from passlib.hash import pbkdf2_sha256
import re
load_dotenv()
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'kasir'
 
mysql = MySQL(app)


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





        
        
        

