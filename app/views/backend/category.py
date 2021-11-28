from flask import render_template, request, jsonify,session
from app import app
from app import db
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
 

@app.route("/category", methods=['GET','POST'])
def category(): 
    
    if request.method == 'POST':
        return redirect(url_for('index'))
    else:
        # koneksi open
        container = []
        conn = db.connect()
        query = conn.execute("SELECT * FROM category") 
        results = query.fetchall()
        # memasukan data dari database ke sql
        for data in results:
            container.append(data)
        conn.close()  
        
        return render_template("backend/pages/category/index.html",container=container)
    
    
