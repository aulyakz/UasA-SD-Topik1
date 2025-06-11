from flask import Flask, render_template, request, redirect, flash, session
from flaskext.mysql import MySQL
app = Flask(__name__)
app.secret_key = 'rahasia'
db=MySQL(host="localhost", user="root", passwd="", db="dbms")
db.init_app(app)

@app.route('/')
def index():
    cursor = db.get_db().cursor()
    cursor.execute("SELECT COUNT(*) FROM user")
    jumlah_user = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM db_guru")
    jumlah_guru = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM db_murid")
    jumlah_murid = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM db_mapel")
    jumlah_mapel = cursor.fetchone()[0]
    return render_template(
        'user/index.html',
        jumlah_user=jumlah_user,
        jumlah_guru=jumlah_guru,
        jumlah_murid=jumlah_murid,
        jumlah_mapel=jumlah_mapel
    )
    return render_template('user/index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM user where username=%s and password=%s",(username,password))
        data = cursor.fetchone()
        if data:
            session['user']=username
            return redirect('/admin/home')
        else:
            flash('Email atau password salah!', 'danger')
            return redirect('/login')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
   
    if request.method == 'POST':
        if str(request.form['password'])!=str(request.form['konfirmasipassword']):
            flash('password dan konfirmasi password tidak cocok!', 'danger')
            return redirect('/register')
        username = request.form['username']
        password = request.form['password']
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM user where username=%s",(username,))
        data = cursor.fetchone()
        if data:
            flash('Maaf, username sudah ada!', 'danger')
            return redirect('/register')
        else:
            cursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (username, password))
            db.get_db().commit()

            flash('Berhasil! Silakan login menggunakan username dan password yang didaftarkan.', 'success')
            return redirect('/login')

    return render_template('register.html')

@app.route('/tentang')
def tentang():
    return render_template('user/tentang.html')

@app.route('/kontak')
def kontak():
    return render_template('user/kontak.html')

@app.route('/sekolah')
def sekolah():
    return render_template('user/sekolah.html')


#  admin

@app.route('/admin/home')
def home():
    if 'user' not in session:
        return redirect('/login')
    cursor = db.get_db().cursor()
    cursor.execute("SELECT COUNT(*) FROM user")
    jumlah_user = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM db_guru")
    jumlah_guru = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM db_murid")
    jumlah_murid = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM db_mapel")
    jumlah_mapel = cursor.fetchone()[0]
    return render_template(
        'admin/index.html',
        jumlah_user=jumlah_user,
        jumlah_guru=jumlah_guru,
        jumlah_murid=jumlah_murid,
        jumlah_mapel=jumlah_mapel
    )
    return render_template('admin/index.html')


@app.route('/admin/admin-guru')
def kelolabarang():
    if 'user' not in session:
        return redirect('/login')
    data=[]
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM db_guru")
        data = cursor.fetchall()
    except Exception as e:
        flash(f"Gagal mengambil data: {e}", "danger")
    return render_template('admin/guru.html', hasil=data)


@app.route('/admin/form-tambah-guru', methods=['GET', 'POST'])
def formbarang():
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        nip = request.form['nip']
        nama = request.form['nama']
        jeniskelamin = request.form['jeniskelamin']
        golpangkat = request.form['golpangkat']
        tempatlahir = request.form['tempatlahir']
        tanggallahir = request.form['tanggallahir']
        alamat= request.form['alamat']
        try:
            cursor = db.get_db().cursor()
            sql = "INSERT INTO db_guru (nip, nama, jeniskelamin, golpangkat, tempatlahir, tanggallahir, alamat) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (nip, nama, jeniskelamin, golpangkat, tempatlahir, tanggallahir, alamat)
            print(val)
            cursor.execute(sql, val)
            db.get_db().commit()
        except Exception as e:
            flash(f'Terjadi kesalahan saat menyimpan data: {e}', 'danger')
        

        flash("Data guru berhasil ditambahkan!", "success")
        return redirect('/admin/admin-guru')
    return render_template('admin/formguru.html')


@app.route('/admin/form-edit-guru/<id>', methods=['GET', 'POST'])
def formeditbarang(id):
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        nip = request.form['nip']
        nama = request.form['nama']
        jeniskelamin = request.form['jeniskelamin']
        golpangkat = request.form['golpangkat']
        tempatlahir = request.form['tempatlahir']
        tanggallahir = request.form['tanggallahir']
        alamat = request.form['alamat']
        try:
            cursor = db.get_db().cursor()
            sql = """
                UPDATE db_guru
                SET nip=%s, nama=%s, jeniskelamin=%s, golpangkat=%s, tempatlahir=%s, tanggallahir=%s, alamat=%s
                WHERE id=%s
            """
            val = (nip, nama, jeniskelamin, golpangkat, tempatlahir, tanggallahir, alamat, id)
            print(val)
            cursor.execute(sql, val)
            db.get_db().commit()
        except Exception as e:
            flash(f'Terjadi kesalahan saat menyimpan data: {e}', 'danger')
        

        flash("Data guru berhasil diupdate!", "success")
        return redirect('/admin/admin-guru')
    data=[]
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM db_guru where id=%s",(id))
        data = cursor.fetchone()
    except Exception as e:
        flash(f'Gagal mengambil data: {e}', 'danger')
        return redirect('/admin/admin-guru')
    return render_template('admin/formeditguru.html', db_guru=data)


@app.route('/admin/hapus-guru/<int:id>', methods=['POST'])
def hapus_barang(id):
    if 'user' not in session:
        return redirect('/login')
    try:
        cursor = db.get_db().cursor()
        cursor.execute("DELETE FROM db_guru WHERE id = %s", (id))
        db.get_db().commit()
        flash("Dara Guru berhasil dihapus.", "success")
    except Exception as e:
        flash(f"Gagal menghapus guru: {e}", "danger")
   

    return redirect('/admin/admin-guru')


@app.route('/admin/admin-murid')
def kelolamurid():
    if 'user' not in session:
        return redirect('/login')
    data=[]
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM db_murid")
        data = cursor.fetchall()
    except Exception as e:
        flash(f"Gagal mengambil data: {e}", "danger")
    return render_template('admin/murid.html', hasil=data)


@app.route('/admin/form-tambah-murid', methods=['GET', 'POST'])
def formmurid():
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        nisn = request.form['nisn']
        nama = request.form['nama']
        jeniskelamin = request.form['jeniskelamin']
        kelas = request.form['kelas']
        tempatlahir = request.form['tempatlahir']
        tanggallahir = request.form['tanggallahir']
        namaibu = request.form['namaibu']
        try:
            cursor = db.get_db().cursor()
            sql = "INSERT INTO db_murid (nisn, nama, jeniskelamin, kelas, tempatlahir, tanggallahir, namaibu) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (nisn, nama, jeniskelamin, kelas, tempatlahir, tanggallahir, namaibu)
            print(val)
            cursor.execute(sql, val)
            db.get_db().commit()
        except Exception as e:
            flash(f'Terjadi kesalahan saat menyimpan data: {e}', 'danger')
        

        flash("Data murid berhasil ditambahkan!", "success")
        return redirect('/admin/admin-murid')
    return render_template('admin/formmurid.html')


@app.route('/admin/form-edit-murid/<id>', methods=['GET', 'POST'])
def formeditmurid(id):
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        nisn = request.form['nisn']
        nama = request.form['nama']
        jeniskelamin = request.form['jeniskelamin']
        kelas = request.form['kelas']
        tempatlahir = request.form['tempatlahir']
        tanggallahir = request.form['tanggallahir']
        namaibu = request.form['namaibu']
        try:
            cursor = db.get_db().cursor()
            sql = """
                UPDATE db_murid
                SET nisn=%s, nama=%s, jeniskelamin=%s, kelas=%s, tempatlahir=%s, tanggallahir=%s, namaibu=%s
                WHERE id=%s
            """
            val = (nisn, nama, jeniskelamin, kelas, tempatlahir, tanggallahir, namaibu, id)
            print(val)
            cursor.execute(sql, val)
            db.get_db().commit()
        except Exception as e:
            flash(f'Terjadi kesalahan saat menyimpan data: {e}', 'danger')
        

        flash("Data murid berhasil diupdate!", "success")
        return redirect('/admin/admin-murid')
    data=[]
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM db_murid where id=%s",(id))
        data = cursor.fetchone()
    except Exception as e:
        flash(f'Gagal mengambil data: {e}', 'danger')
        return redirect('/admin/admin-murid')
    return render_template('admin/formeditmurid.html', db_murid=data)


@app.route('/admin/hapus-murid/<int:id>', methods=['POST'])
def hapus_murid(id):
    if 'user' not in session:
        return redirect('/login')
    try:
        cursor = db.get_db().cursor()
        cursor.execute("DELETE FROM db_murid WHERE id = %s", (id))
        db.get_db().commit()
        flash("murid berhasil dihapus.", "success")
    except Exception as e:
        flash(f"Gagal menghapus murid: {e}", "danger")
   
    return redirect('/admin/admin-mapel')

@app.route('/admin/admin-mapel')
def kelolamapel():
    if 'user' not in session:
        return redirect('/login')
    data=[]
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM db_mapel")
        data = cursor.fetchall()
    except Exception as e:
        flash(f"Gagal mengambil data: {e}", "danger")
    return render_template('admin/mapel.html', hasil=data)


@app.route('/admin/form-tambah-mapel', methods=['GET', 'POST'])
def formmapel():
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        kode = request.form['kode']
        mapel = request.form['mapel']
        jam = request.form['jam']
        hari = request.form['hari']
        kelas = request.form['kelas']
        guru = request.form['guru']
        try:
            cursor = db.get_db().cursor()
            sql = "INSERT INTO db_mapel (kode, mapel, jam, hari, kelas, guru) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (kode, mapel, jam, hari, kelas, guru)
            print(val)
            cursor.execute(sql, val)
            db.get_db().commit()
        except Exception as e:
            flash(f'Terjadi kesalahan saat menyimpan data: {e}', 'danger')
        

        flash("Data Mapel berhasil ditambahkan!", "success")
        return redirect('/admin/admin-mapel')
    return render_template('admin/formmapel.html')


@app.route('/admin/form-edit-mapel/<id>', methods=['GET', 'POST'])
def formeditmapel(id):
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        kode = request.form['kode']
        mapel = request.form['mapel']
        jam = request.form['jam']
        hari = request.form['hari']
        kelas = request.form['kelas']
        guru = request.form['guru']
        try:
            cursor = db.get_db().cursor()
            sql = """
                UPDATE db_mapel
                SET kode=%s, mapel=%s, jam=%s, hari=%s, kelas=%s, guru=%s
                WHERE id=%s
            """
            val= (kode, mapel, jam, hari, kelas, guru, id)
            print(val)
            cursor.execute(sql, val)
            db.get_db().commit()
        except Exception as e:
            flash(f'Terjadi kesalahan saat menyimpan data: {e}', 'danger')
        

        flash("Data Mapel berhasil diupdate!", "success")
        return redirect('/admin/admin-mapel')
    data=[]
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM db_mapel where id=%s",(id))
        data = cursor.fetchone()
    except Exception as e:
        flash(f'Gagal mengambil data: {e}', 'danger')
        return redirect('/admin/admin-mapel')
    return render_template('admin/formeditmapel.html', db_mapel=data)


@app.route('/admin/hapus-mapel/<int:id>', methods=['POST'])
def hapus_mapel(id):
    if 'user' not in session:
        return redirect('/login')
    try:
        cursor = db.get_db().cursor()
        cursor.execute("DELETE FROM db_mapel WHERE id = %s", (id))
        db.get_db().commit()
        flash("Mapel berhasil dihapus.", "success")
    except Exception as e:
        flash(f"Gagal menghapus mapel: {e}", "danger")
   

    return redirect('/admin/admin-mapel')






@app.route('/admin/admin-kelola-pengguna')
def kelolapengguna():
    if 'user' not in session:
        return redirect('/login')
    data=[]
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM user")
        data = cursor.fetchall()
    except Exception as e:
        flash(f"Gagal mengambil data: {e}", "danger")
    return render_template('admin/pengguna.html', hasil=data)



@app.route('/admin/admin-kelola-user')
def kelolauser():
    if 'user' not in session:
        return redirect('/login')
    data=[]
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM user")
        data = cursor.fetchall()
    except Exception as e:
        flash(f"Gagal mengambil data: {e}", "danger")
    return render_template('admin/user.html', hasil=data)


@app.route('/admin/form-tambah-user', methods=['GET', 'POST'])
def formuser():
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
       
        try:
            cursor = db.get_db().cursor()
            sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
            val = (username, password)
            print(val)
            cursor.execute(sql, val)
            db.get_db().commit()
        except Exception as e:
            flash(f'Terjadi kesalahan saat menyimpan data: {e}', 'danger')
        

        flash("Data user berhasil ditambahkan!", "success")
        return redirect('/admin/admin-kelola-user')
    return render_template('admin/formuser.html')

@app.route('/admin/form-edit-user/<id>', methods=['GET', 'POST'])
def formedituser(id):
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
       
        try:
            cursor = db.get_db().cursor()
            sql = """
                UPDATE user
                SET username=%s, password=%s
                WHERE id=%s
            """
            val = (username, password,id)
            print(val)
            cursor.execute(sql, val)
            db.get_db().commit()
        except Exception as e:
            flash(f'Terjadi kesalahan saat menyimpan data: {e}', 'danger')
        

        flash("Data user berhasil diupdate!", "success")
        return redirect('/admin/admin-kelola-user')
    data=[]
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM user where id=%s",(id))
        data = cursor.fetchone()
    except Exception as e:
        flash(f'Gagal mengambil data: {e}', 'danger')
        return redirect('/admin/admin-kelola-user')
    return render_template('admin/formedituser.html', user=data)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
