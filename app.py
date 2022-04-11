from sqlite3 import Row
from flask import Flask, render_template, \
    request, redirect, url_for, session, flash
import pymysql.cursors, os


application = Flask(__name__)
application.secret_key = 'iloveikutalilas'

conn = cursor = None
#fungsi koneksi ke db
def openDb():
   global conn, cursor
   conn = pymysql.connect(host='localhost',user='root',password='',database='db_gunpla')
   cursor = conn.cursor()	
   
#fungsi menutup koneksi
def closeDb():
    global conn, cursor
    cursor.close()
    conn.close()
    
@application.route('/')  
@application.route('/login', methods = ['POST', 'GET'])
def login():
    openDb()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username = %s and password = %s", (username, password,))
        user = cursor.fetchone()
        if user:
            session['logged_in'] = True
            session['username']=user("username")
            return redirect(url_for('home'))
    return render_template('login.html')

@application.route("/logout")
def logout():
	session.clear()
	flash('You are now logged out','success')
	return redirect(url_for('login'))
    
#fungsi view index menampilkan data dri db
@application.route('/index')
def index():
    openDb()
    container = []
    sql = "SELECT * FROM gunpla"
    cursor.execute(sql)
    results = cursor.fetchall()
    for data in results:
        container.append(data)
    closeDb()
    return render_template('index.html', container=container,)

#fungsi view tambah() untuk membuat form tambah
@application.route('/tambah', methods=['GET','POST'])
def tambah():
    if request.method == 'POST':
        nama_gundam = request.form['nama_gundam']
        grade = request.form['grade']
        harga = request.form['harga']
        stok = request.form['stok']
        openDb()
        sql = "INSERT INTO gunpla (nama_gundam, grade, harga, stok) VALUES (%s, %s, %s, %s)"
        val = (nama_gundam, grade, harga, stok)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()
        return redirect(url_for('index'))
    else:
        return render_template('tambah.html')
    
#fungsi view edit() buat form edit
@application.route('/edit/<id_gunpla>', methods= ['GET','POST'])
def edit(id_gunpla):
   openDb()
   cursor.execute('SELECT * FROM gunpla WHERE id_gunpla=%s', (id_gunpla))
   data = cursor.fetchone()
   if request.method == 'POST':
       id_gunpla = request.form['id_gunpla']
       nama_gundam = request.form['nama_gundam']
       grade = request.form['grade']
       harga = request.form['harga']
       stok = request.form['stok']
       sql = "UPDATE gunpla SET nama_gundam=%s, grade=%s, harga=%s, stok=%s WHERE id_gunpla=%s"
       val = (nama_gundam, grade, harga, stok, id_gunpla)
       cursor.execute(sql, val)
       conn.commit()
       closeDb()
       return redirect(url_for('index'))
   else:
       closeDb()
       return render_template('edit.html', data=data)
   
#fungsi haous data
@application.route('/hapus/<id_gunpla>', methods=['GET','POST'])
def hapus(id_gunpla):
   openDb()
   cursor.execute('DELETE FROM gunpla WHERE id_gunpla=%s', (id_gunpla))
   conn.commit()
   closeDb()
   return redirect(url_for('index'))


if __name__ == '__main__':
    application.run(debug=True)
    