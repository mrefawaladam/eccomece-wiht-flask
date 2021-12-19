from flask import render_template, redirect, request, jsonify,session,url_for
from app import app
from app import db  
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename  



app.config["UPLOAD_FOLDER"] = "app/static/upload/product/"


@app.route("/product", methods=['GET','POST'])
def product(): 
    
    if request.method == 'POST':

        return redirect(url_for('index'))
    else:
        # koneksi open
        container = []
        conn = db.connect()
        query = conn.execute("SELECT p.*, sc.name as nama_sub_categoi, c.name as nama_categoi FROM product as p INNER JOIN sub_category sc ON p.id_sub_category = sc.id_sub_category INNER JOIN category c ON c.id_category = sc.category_id") 
        results = query.fetchall()
        # memasukan data dari database ke sql
        for data in results:
            container.append(data)
        conn.close()  
        
        return render_template("backend/pages/product/index.html",container=container)
    

@app.route("/product/create", methods=['GET','POST'])
def productCreate(): 
    if request.method == 'POST':
        conn = db.connect()
        files = request.files['file']
        name = request.form.get('name')
        id_sub_category = request.form.get('id_sub_category')
        price = request.form.get('price')
        qty = request.form.get('qty')
        weight = request.form.get('weight') 
        description = request.form.get('description') 


        # prose upload foto
        filename = secure_filename(files.filename)
        files.save(app.config['UPLOAD_FOLDER'] + filename)
 
        query = 'Insert Into product (name, description,id_sub_category, price,qty,weight,main_image	) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}");'.format(
        name,description,id_sub_category,price,qty,weight, filename )
        conn.execute(query)
        conn.close()
        return redirect(url_for('product'))
    else:
        category = []
        conn = db.connect()
        query = conn.execute("SELECT * FROM sub_category") 
        results = query.fetchall()
        # memasukan data dari database ke sql
        for data in results:
            category.append(data)
        conn.close()  
        return render_template("backend/pages/product/create.html",category=category)


@app.route("/product/edit/<id_category>", methods=['GET','POST'])
def productEdit(id_category): 
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
        return render_template("backend/pages/product/edit.html",dataCategory=dataCategory)

@app.route("/product/delete/<id_category>" )
def productDelete(id_category): 
    conn = db.connect()
    query = conn.execute("DELETE FROM category WHERE id_category=%s",(id_category)) 
    conn.close()
    return redirect(url_for('category'))