from flask import Flask
from flask import render_template, request
#from flask.helpers import url_for
from flaskext.mysql import MySQL
#from pymysql import connections, cursors
#from werkzeug import datastructures
from werkzeug.utils import redirect
import re
app = Flask(__name__)

mysql= MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='tutorias'
mysql.init_app(app)

@app.route('/')
def index():
    return render_template('student/index.html')

@app.route('/login')
def login():
    return render_template('student/login.html')

@app.route('/master-login')
def master_login():
    return render_template('tutor/login.html')

@app.route('/suggest')
def suggest():
    return render_template('student/suggest.html')

@app.route('/updated')
def updated():
    return render_template('handling/sucess/updated.html')

@app.route('/created')
def created():
    return render_template('handling/sucess/created.html')

@app.route('/error-update')
def error_update():
    return render_template('handling/error/error-update.html')

@app.route('/error-save')
def error_save():
    return render_template('handling/error/error-save.html')

@app.route('/error-404')
def error_404():
    return render_template('handling/error/error-404.html')

@app.route('/error-form')
def error_form():
    return render_template('handling/error/error-form.html')

@app.route('/error-login-student')
def error_login_student():
    return render_template('handling/error/error-login-student.html')

@app.route('/error-login-master')
def error_login_master():
    return render_template('handling/error/error-login-master.html')


@app.route('/tutors')
def tutors():
    try:
        sql = "SELECT tutores.id_tutor, tutores.nombre, tutores.correo, carreras.nombre AS carrera, alumnos.nombre AS alumnos FROM alumnos INNER JOIN carreras ON alumnos.id_carrera = carreras.id_carrera INNER JOIN tutores ON alumnos.id_tutor = tutores.id_tutor;";
        connection= mysql.connect()
        cursor = connection.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        print(data)
        connection.commit()
        return render_template('tutor/tutors.html', data=data)
    except Exception as e:
        return redirect('/error-form')


@app.route('/students')
def students():
    try:
        sql = "SELECT alumnos.id_alumno, alumnos.nombre, alumnos.correo, alumnos.codigo, carreras.nombre AS carrera, tutores.nombre AS tutor FROM alumnos INNER JOIN carreras ON alumnos.id_carrera = carreras.id_carrera INNER JOIN tutores ON alumnos.id_tutor = tutores.id_tutor;";
        connection= mysql.connect()
        cursor = connection.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        connection.commit()
        return render_template('tutor/students.html', data=data)
    except Exception as e:
        return redirect('/error-form')

@app.route('/form')
def form():
    try:
        sql = "SELECT preguntas.id_pregunta, preguntas.pregunta, preguntas.respuesta, keyword, etapas.etapa FROM preguntas JOIN etapas ON preguntas.id_etapa = etapas.id_etapa";
        connection= mysql.connect()
        cursor = connection.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        connection.commit()
        return render_template('tutor/form.html', data=data)
    except Exception as e:
        print(e)
        return redirect('/error-form')


@app.route('/edit-question/<int:id>')
def edit_question(id):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM preguntas WHERE id_pregunta=%s",(id))
        data = cursor.fetchall()
        connection.commit()
        return render_template('tutor/edit-question.html', data = data)
    except Exception as e:
        print(e)



@app.route('/update', methods=['POST'])
def update():
    try:
        id_question = request.form['id']
        question = request.form['pregunta']
        answer = request.form['respuesta']
        keyword = request.form['keyword']
        stage = request.form['stage']
        if id_question and question and answer and keyword and stage and request.method == 'POST':
            sql = "UPDATE preguntas SET pregunta=%s,respuesta=%s,keyword=%s, id_etapa=%s WHERE id_pregunta=%s;"
            data =(question,answer,keyword,stage,id_question)
            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute(sql,data)
            connection.commit()
            row = cursor.fetchone()
            return redirect('updated')
        else:
            return redirect('error-update')
    except Exception as e:
        print(e)

@app.route('/new-question')
def new_question():
    return render_template('tutor/new-question.html')

@app.route('/get')
def get():
    userText = request.args.get('msg')
    if userText == "tutores":
        connection = mysql.connect()
        cursor=connection.cursor()
        cursor.execute("SELECT alumnos.nombre, tutores.nombre AS tutor FROM alumnos INNER JOIN tutores ON alumnos.id_tutor = tutores.id_tutor;")
        connection.commit()
        data = cursor.fetchall()
        result = " ".join(str(x) for x in data)
        result = result.replace("(","").replace(")","\n").replace("'","").replace("\\n"," ").replace("\\r","  ").replace("\\"," ")
        print("Con gusto:\n"+result)
        return str("Con gusto:\n"+result)
    else:
        connection = mysql.connect()
        cursor=connection.cursor()
        cursor.execute("SELECT respuesta FROM preguntas WHERE keyword='"+userText+"'")
        connection.commit()
        data = cursor.fetchall()
        result = " ".join(str(x) for x in data)
        result = result.replace("(","").replace(")","").replace("'","").replace("\\n"," ").replace("\\r"," ").replace("\\"," ")
        result = result.replace(","," ")
        print(result)
        return str(result)

@app.route('/storage', methods=['POST'])
def storage():
    try:
        question = request.form['pregunta']
        answer = request.form['respuesta']
        keyword = request.form['keyword']
        stage = request.form['stage']
        connection = mysql.connect()
        cursor = connection.cursor()
        if question and answer and keyword and stage and request.method == 'POST':
            sql = "INSERT INTO `preguntas` (`id_pregunta`, `pregunta`, `respuesta`, `keyword`, `id_etapa`) VALUES (NULL, %s, %s, %s, %s);"
            data = (question, answer, keyword, stage)
            cursor.execute(sql,data)
            connection.commit()
            return redirect('created')
        else:
            return redirect('error-save')
    except Exception as e:
        print(e)

@app.route('/verify-student', methods=['POST'])
def verify_student():
    studentCode = request.form['code']
    if studentCode and re.match("^[0-9]{9}$[ ]{0}", studentCode) and request.method == 'POST':
        connection = mysql.connect()
        cursor=connection.cursor()
        cursor.execute("SELECT codigo FROM alumnos WHERE codigo='"+studentCode+"'")
        connection.commit()
        data = cursor.fetchall()
        result = " ".join(str(x) for x in data)
        result = result.replace("(","").replace(")","").replace(","," ").replace(" ","")
        if studentCode == result:       
            return redirect('/')
    return redirect('/error-login-student')

@app.route('/verify-master', methods=['POST'])
def verify_master():
    pwd = request.form['pwd']
    if pwd == '123' and request.method == 'POST':
        return redirect('/form')
    else:
        return redirect('/error-login-master')

if __name__== '__main__':
    app.run(debug=True)
