 
from flask import render_template, redirect,request, jsonify,session
from app import app
from app import db
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

app.secret_key = 'fadsf332rdse'

# proses registrasi ke database
@app.route("/storeregistrasi", methods=['POST'])
def storeregistrasi(): 
    conn = db.connect()

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')  
    username = request.form.get('username')
    password = request.form.get('password') 
    email = request.form.get('email')
    hash_password = generate_password_hash(password, method='sha256')

    query = 'Insert Into user (first_name, last_name,    username, password , email) VALUES ("{}", "{}", "{}", "{}", "{}");'.format(
        first_name, last_name ,username,hash_password ,email)
    conn.execute(query)
    conn.close()
    return render_template("frontend/auth/register.html" )
    
# register
@app.route("/registrasi")
def registrasi(): 
    return render_template("frontend/auth/register.html" )

# login
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
        # koneksi close
        if not user:
            return "Error user not found"
        else:
            if  check_password_hash(user.password, password):
                session['name'] = user.first_name
                session['username'] = user.username
                return redirect("dashboard-admin", code=200)
            else:
                return "Error password and username not match"
    else:
        return render_template("frontend/auth/login.html")