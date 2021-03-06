from flask import render_template, redirect, request, jsonify,session,url_for
from app import app
from app import db
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename  
 

app.config["UPLOAD_FOLDER"] = "app/static/upload/categori/"

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
    

@app.route("/category/create", methods=['GET','POST'])
def categoryCreate(): 
    if request.method == 'POST':
        conn = db.connect()
        files = request.files['file']
        name = request.form.get('name')
        # prose upload foto
        filename = secure_filename(files.filename)
        files.save(app.config['UPLOAD_FOLDER'] + filename)
 
        query = 'Insert Into category (name, image) VALUES ("{}", "{}");'.format(
        name, filename )
        conn.execute(query)
        conn.close()
        return redirect(url_for('category'))
    else:
        return render_template("backend/pages/category/create.html")


@app.route("/category/edit/<id_category>", methods=['GET','POST'])
def categoryEdit(id_category): 
    conn = db.connect()
    query = conn.execute("SELECT * FROM category WHERE id_category=%s",(id_category)) 
    dataCategory = query.fetchone()
    if request.method == 'POST':
        
        files = request.files['file']
        name = request.form.get('name')
        # prose upload foto
        if(files):
            filename = secure_filename(files.filename)
            files.save(app.config['UPLOAD_FOLDER'] + filename)
        else:
            filename = dataCategory[2]
        query = 'Insert Into category (name, image) VALUES ("{}", "{}");'.format(
        name, filename )
        conn.execute(query)
        conn.close()
        return redirect(url_for('category'))
    else:
        conn.close() 
        return render_template("backend/pages/category/edit.html",dataCategory=dataCategory)

@app.route("/category/delete/<id_category>" )
def categoryDelete(id_category): 
    conn = db.connect()
    query = conn.execute("DELETE FROM category WHERE id_category=%s",(id_category)) 
    conn.close()
    return redirect(url_for('category'))