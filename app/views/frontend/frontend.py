from flask import render_template, request, jsonify,session
from app import app
from app import db
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from pprint import pprint 
import json


@app.route("/shop", methods=['GET'])
def shop(): 
    product = []
    category = []

    conn = db.connect()
    # data produk
    queryProduct = conn.execute("SELECT * FROM product ") 
    resultsProduct = queryProduct.fetchall()
 
    # memasukan data dari database ke sql
    for data in resultsProduct: 
        product.append(data ) 

     # data categroy
    queryCategory = conn.execute("SELECT * FROM category ") 
    resultCategory = queryCategory.fetchall()
 
    querySubCategory = conn.execute("SELECT * FROM sub_category ") 
    resultSubCategory = querySubCategory.fetchall()
   

    conn.close()   


    return render_template("frontend/pages/produk/index.html",product=product,resultCategory=resultCategory,resultSubCategory=resultSubCategory)
    
    
@app.route("/shop/<id_product>" )
def shopDetail(id_product): 
    conn = db.connect()
    query = conn.execute("SELECT * FROM product WHERE id_product=%s",(id_product)) 
    dataProduct = query.fetchone()
    conn.close()
    return render_template("frontend/pages/produk/detail.html",dataProduct=dataProduct)

@app.route("/")
def homepage(): 
    conn = db.connect()
    query = conn.execute("SELECT * FROM product  ") 
    dataProduct = query.fetchall()
    conn.close()
    return render_template("index.html" )

@app.route("/shop/search" , methods=['post'])
def shopSearch(): 
    conn = db.connect()
    search = request.form.get('search').split('%')

    
    query = conn.execute("SELECT * FROM product WHERE name LIKE %s",(search )) 
    product = query.fetchall()

    queryCategory = conn.execute("SELECT * FROM category ") 
    resultCategory = queryCategory.fetchall()
 
    querySubCategory = conn.execute("SELECT * FROM sub_category ") 
    resultSubCategory = querySubCategory.fetchall()
   

    conn.close()
    return render_template("frontend/pages/produk/index.html",product=product,resultCategory=resultCategory,resultSubCategory=resultSubCategory)

@app.route("/analitic")
def analitic(): 
    conn = db.connect()
    start_date = '2021-01-18' 
    end_date = '2021-12-30' 

    queryCategory = conn.execute("SELECT * FROM category ") 
    resultCategory = queryCategory.fetchall()
 
    querySubCategory = conn.execute("SELECT * FROM sub_category ") 
    resultSubCategory = querySubCategory.fetchall()
   

    queryAnalitic = conn.execute("SELECT p.name, SUM(td.qty) Jumlah, t.date_transaction FROM transaction t INNER JOIN transaction_detail td ON t.id_transaction = td.transaction_id INNER JOIN product p ON p.id_product = td.product_id INNER JOIN sub_category sc ON p.id_sub_category = sc.id_sub_category INNER JOIN category c ON c.id_category = sc.category_id WHERE t.date_transaction BETWEEN %s AND %s  GROUP BY p.id_product ORDER BY COUNT(p.id_product) DESC ",(start_date,end_date)) 
    resultAnalitic = queryAnalitic.fetchall()
  
    lebel = [] 
    jumlah = [] 
    votes = [] 



    for data in resultAnalitic: 
        lebel.append(data[0] ) 
        jumlah.append(str(data[1]) ) 
        votes.append(str(data[2])                                            ) 
 

    conn.close()
    return render_template("frontend/pages/analitic/index.html", resultCategory=resultCategory,resultSubCategory=resultSubCategory,jumlah=jumlah,lebel=lebel,votes=votes)

@app.route("/analitic/search", methods=['post'])
def analiticSearch(): 
    conn = db.connect()
    start_date = request.form.get('start_date') 
    end_date = request.form.get('end_date') 
    categori = request.form.get('categori') 
    sub_categori = request.form.get('sub_categori') 
   


    queryCategory = conn.execute("SELECT * FROM category ") 
    resultCategory = queryCategory.fetchall()
 
    querySubCategory = conn.execute("SELECT * FROM sub_category ") 
    resultSubCategory = querySubCategory.fetchall()
   

    queryAnalitic = conn.execute("SELECT p.name, SUM(td.qty) Jumlah, t.date_transaction FROM transaction t INNER JOIN transaction_detail td ON t.id_transaction = td.transaction_id INNER JOIN product p ON p.id_product = td.product_id INNER JOIN sub_category sc ON p.id_sub_category = sc.id_sub_category INNER JOIN category c ON c.id_category = sc.category_id WHERE t.date_transaction BETWEEN %s AND %s AND c.name = %s AND sc.name = %s GROUP BY p.id_product ORDER BY COUNT(p.id_product) DESC ",(start_date,end_date,categori,sub_categori)) 
    resultAnalitic = queryAnalitic.fetchall()
  
    lebel = [] 
    jumlah = [] 
    votes = [] 



    for data in resultAnalitic: 
        lebel.append(data[0] ) 
        jumlah.append(str(data[1]) ) 
        votes.append(str(data[2])                                            ) 
 
    conn.close()
    return render_template("frontend/pages/analitic/index.html", resultCategory=resultCategory,resultSubCategory=resultSubCategory,jumlah=jumlah,lebel=lebel,votes=votes)




