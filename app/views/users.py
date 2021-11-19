 
from flask import render_template, request, jsonify,session
from app import app
from app import db
import bcrypt
  

@app.route("/storeregistrasi", methods=['POST'])
def storeregistrasi(): 
    conn = db.connect()

    first_name = request.form['first_name']
    last_name = request.form['last_name']  
    username = request.form['username']
    password = request.form['password'].encode('utf-8')
    email = request.form['email']
    hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

    query = 'Insert Into user (first_name, last_name,    username, password , email) VALUES ("{}", "{}", "{}", "{}", "{}");'.format(
        first_name, last_name ,username,hash_password ,email)
    conn.execute(query)
    conn.close()
    return render_template("frontend/auth/register.html" )
    

@app.route("/registrasi")
def registrasi(): 
    return render_template("frontend/auth/register.html" )

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        # koneksi open
        conn = db.connect()

        
        query = conn.execute("SELECT * FROM user WHERE username=%s",(username,)) 
        user = query.fetchone()
        conn.close() 

        if len(user) > 0:
            if bcrypt.check_password_hash(user['password'], form.password.data):
                session['name'] = user['name']
                session['username'] = user['username']
                return render_template("home.html")
            else:
                return "Error password and username not match"
        else:
            return "Error user not found"
    else:
        return render_template("frontend/auth/login.html")