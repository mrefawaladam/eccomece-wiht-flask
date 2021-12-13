from flask import render_template, redirect, request, jsonify,session,url_for
from app import app
from app import db


@app.route("/sub-category", methods=['GET','POST'])
def subCategory(): 
    
    if request.method == 'POST':

        return redirect(url_for('index'))
    else:
        # koneksi open
        container = []
        conn = db.connect()
        query = conn.execute("SELECT sub_category.id_sub_category	, category.name as nama_categori,sub_category.name as nama_sub_categori  FROM sub_category inner join category on category.id_category = sub_category.category_id") 
        results = query.fetchall()
        # memasukan data dari database ke sql
        for data in results:
            container.append(data)
        conn.close()  
                                                                                
        return render_template("backend/pages/sub_category/index.html",container=container)
    

@app.route("/sub-category/create", methods=['GET','POST'])
def subCategoryCreate(): 
    if request.method == 'POST':
        conn = db.connect() 
        name = request.form.get('name')
        category_id = request.form.get('category_id')

       
        query = 'Insert Into sub_category (name, category_id) VALUES ("{}", "{}");'.format(
        name, category_id )
        conn.execute(query)
        conn.close()
        return redirect(url_for('subCategory'))
    else:
        container = []
        conn = db.connect()
        query = conn.execute("SELECT * FROM category") 
        results = query.fetchall()
        # memasukan data dari database ke sql
        for data in results:
            container.append(data)
        conn.close() 
        return render_template("backend/pages/sub_category/create.html",container=container)


@app.route("/sub-category/edit/<id_sub_category>", methods=['GET','POST'])
def subCategoryEdit(id_sub_category): 
    conn = db.connect()
    query = conn.execute("SELECT * FROM category WHERE id_sub_category=%s",(id_sub_category)) 
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
        return render_template("backend/pages/sub_category/edit.html",dataCategory=dataCategory)

@app.route("/sub-category/delete/<id_sub_category>" )
def subCategoryDelete(id_sub_category): 
    conn = db.connect()
    query = conn.execute("DELETE FROM category WHERE id_sub_category=%s",(id_sub_category)) 
    conn.close()
    return redirect(url_for('category'))