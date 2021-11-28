from flask import render_template, request, jsonify,session
from app import app
from app import db
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
 

@app.route("/dashboard-admin", methods=['GET'])
def dashboard_admin(): 
    return render_template("backend/layouts/app.html")
    
    
