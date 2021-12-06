from flask import Flask
from flask import render_template, request, session
from datetime import timedelta
from flaskext.mysql import MySQL #Install
from werkzeug.utils import redirect
from functools import wraps
from flask_mail import Mail, Message # Install
import re

app = Flask(__name__)
#With os 
#os.random(24)
app.config['SECRET_KEY'] = 'secret-key:)'
mysql= MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='tutorias'
mysql.init_app(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'soysolarelbot@gmail.com'
app.config['MAIL_PASSWORD'] = 'jitgirosvbiigney'
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'pwd' in session:
            return f(*args, **kwargs)
        else:
            return "Logueate nuevamente"
    return wrap

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'studentCode' in session:
            return f(*args, **kwargs)
        else:
            return "Logueate nuevamente"
    return wrap

@app.route('/solar')
@app.route('/chatbot')
def index():
    return render_template('student/index.html')

@app.route('/login')
def login():
    return render_template('student/login.html')

@app.route('/')
def home():
        return render_template('home.html')

@app.route('/suggest')
@login_required
def suggest():
    return render_template('student/suggest.html')

@app.route('/master-login')
def master_login():
    return render_template('tutor/login.html')

@app.route('/new-question')
@admin_required
def new_question():
    return render_template('tutor/new-question.html')

@app.route('/new-tutor')
@admin_required
def new_tutor():
    return render_template('tutor/new-tutor.html')


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

#Handling Errors

@app.errorhandler(400)
def handle_bad_request(e):
    return render_template('handling/error/error-400.html'), 400

@app.errorhandler(403)
def handle_bad_request(e):
    return render_template('handling/error/error-400.html'), 403

@app.errorhandler(404)
def not_found(self):
    return render_template('handling/error/error-404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('handling/error/error-500.html'), 500

@app.errorhandler(405)
def method_not_found(error):
    return render_template('handling/error/error-405.html'), 405

@app.route('/error-500')
def error_500():
    return render_template('handling/error/error-500.html')

@app.route('/error-405')
def error_405():
    return render_template('handling/error/error-405.html')

@app.route('/error-400')
def error_400():
    return render_template('handling/error/error-400.html')

@app.route('/error-form')
def error_form():
    return render_template('handling/error/error-form.html')


@app.route("/sending-email", methods=['POST','GET'])
@login_required
def sending_email():
    if request.method == "POST":
        msg = Message("¡Nueva Pregunta Sugerida!", sender= 'soysolarelbot@gmail.com',recipients= ["soysolarelbot@gmail.com"])
        msg.body = "¡Hola, Administrador!\n ¡Un alumno ha enviado una nueva sugerencia!\n"+"Pregunta: "+request.form.get("body")+"\n¡Chécalo!"
        with app.open_resource("static/images/character/new-suggest.jpeg") as fp:
            msg.attach("new-suggest.jpeg", "image/jpeg", fp.read())
        mail.send(msg)
        return render_template("student/result-email.html", result="Success")
    else:
       return render_template("student/result-email.html", result="Failure")

@app.route('/tutor-and-student')
@admin_required
def tutor_and_student():
    try:
        sql = "SELECT tutores.id_tutor, tutores.nombre, tutores.correo,carreras.id_carrera, carreras.nombre AS carrera, alumnos.id_alumno, alumnos.nombre AS alumnos FROM alumnos INNER JOIN carreras ON alumnos.id_carrera = carreras.id_carrera INNER JOIN tutores ON alumnos.id_tutor = tutores.id_tutor";
        connection= mysql.connect()
        cursor = connection.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        connection.commit()
        return render_template('tutor/tutor-and-student.html', data=data)
    except KeyError as e:
        print(e)
        return render_template('/error-form')

@app.route('/tutors')
@admin_required
def tutors():
    try:
        sql = "SELECT tutores.id_tutor, tutores.nombre, tutores.correo, carreras.id_carrera, carreras.nombre AS carreras FROM tutores INNER JOIN carreras ON tutores.id_carrera = carreras.id_carrera;";
        connection= mysql.connect()
        cursor = connection.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        connection.commit()
        return render_template('tutor/tutors.html', data=data)
    except KeyError as e:
        print(e)
        return render_template('/error-form')

@app.route('/edit-tutor/<int:id_tutor>/<int:id_career>/')
@admin_required
def edit_tutor(id_tutor,id_career):
    try:
        if session['pwd'] != session:
            try:
                connection = mysql.connect()
                cursor = connection.cursor()
                cursor.execute("SELECT tutores.id_tutor, tutores.nombre, tutores.correo, carreras.id_carrera, carreras.nombre AS carreras FROM tutores INNER JOIN carreras ON tutores.id_carrera = carreras.id_carrera WHERE tutores.id_tutor=%s AND tutores.id_carrera=%s",(id_tutor,id_career)) 
                data = cursor.fetchall()
                connection.commit()
                return render_template('tutor/edit-tutor.html', data=data)
            except Exception as e:
                print(e)
                return render_template('handling/error/error-edit-tutor.html')
    except KeyError as e:
        print(e)
        return "Error"

@app.route('/edit-students/<int:id_student>/<int:id_career>/')
@admin_required
def edit_students(id_student,id_career):
    try: 
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT alumnos.id_alumno, alumnos.nombre, alumnos.correo, alumnos.codigo, carreras.id_carrera, carreras.nombre AS carreras FROM alumnos INNER JOIN carreras ON alumnos.id_carrera = carreras.id_carrera WHERE alumnos.id_alumno =%s AND alumnos.id_carrera = %s;",(id_student,id_career))
        data = cursor.fetchall()
        connection.commit()
        return render_template('tutor/edit-students.html', data=data)
    except KeyError as e:
        print(e)
        return redirect('/error-form')
    return redirect('/error-form')

@app.route('/students')
@admin_required
def students():
    try: 
        sql = "SELECT alumnos.id_alumno, alumnos.nombre, alumnos.correo, alumnos.codigo, carreras.id_carrera, carreras.nombre AS carreras FROM alumnos INNER JOIN carreras ON alumnos.id_carrera = carreras.id_carrera;";
        connection= mysql.connect()
        cursor = connection.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        connection.commit()
        return render_template('tutor/students.html', data=data)
    except KeyError as e:
        print(e)
        return redirect('/error-form')
    return redirect('/error-form')

@app.route('/edit-tutor-and-student.html')
@admin_required
def edit_tutor_and_student():
    try: 
        sql = "SELECT tutores.id_tutor, tutores.nombre, tutores.correo,carreras.id_carrera, carreras.nombre AS carrera, alumnos.id_alumno, alumnos.nombre AS alumnos FROM alumnos INNER JOIN carreras ON alumnos.id_carrera = carreras.id_carrera INNER JOIN tutores ON alumnos.id_tutor = tutores.id_tutor";
        connection= mysql.connect()
        cursor = connection.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.fetchone()
        connection.commit()
        return render_template('tutor/students.html', data=data)
    except KeyError as e:
        print(e)
        return redirect('/error-form')
    return redirect('/error-form')

@app.route('/form')
@admin_required
def form():
    try:
        try:
            sql = "SELECT preguntas.id_pregunta, preguntas.pregunta, preguntas.respuesta, keyword, etapas.etapa FROM preguntas JOIN etapas ON preguntas.id_etapa = etapas.id_etapa";
            connection= mysql.connect()
            cursor = connection.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            connection.commit()
            return render_template('tutor/form.html', data=data)
        except mysql.connector.Error as err:
            print(err)
            return redirect('/error-form')
    except KeyError as e:
        print(e)
        return redirect('/error-form')


@app.route('/edit-question/<int:id>')
@admin_required
def edit_question(id):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM preguntas WHERE id_pregunta=%s",(id)) 
        data = cursor.fetchall()
        connection.commit()
        return render_template('tutor/edit-question.html', data = data)
    except KeyError as e:
        print(e)
        return "Error"


@app.route('/update', methods=['POST'])
@admin_required
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
            return render_template('handling/sucess/updated.html')
        else:
            return render_template('handling/error/error-update.html')
    except KeyError as e:
        print(e)
        return render_template('handling/error/error-update.html')

@app.route('/update-tutor', methods=['POST'])
@admin_required
def update_tutor():
    try:
        tutor_id = request.form['tutor_id']
        tutor_name = request.form['tutor_name']
        tutor_email = request.form['tutor_email']
        tutor_career = request.form['tutor_career']
        if tutor_id and tutor_name and tutor_email and tutor_career and request.method == 'POST':
            sql = "UPDATE `tutores` SET `nombre` = %s, `correo` =%s, `id_carrera` = %s WHERE `tutores`.`id_tutor` = %s;"
            data =(tutor_name,tutor_email,tutor_career,tutor_id)
            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute(sql,data)
            connection.commit()
            row = cursor.fetchone()
            return render_template('handling/sucess/updated.html')
        else:
            return render_template('handling/error/error-update.html')
    except KeyError as e:
        print(e)
        return render_template('handling/error/error-update.html')
    return "Error"

@app.route('/update-students', methods=['POST'])
@admin_required
def update_students():
    try:
        id_student= request.form['id_student']
        id_career= request.form['id_career']
        name_student = request.form['name_student']
        email_student = request.form['email_student']
        code_student = request.form['code_student']
        career_student = request.form['career_student']
        if id_student and id_career and name_student and email_student and code_student and career_student  and request.method == 'POST':
            sql = "UPDATE alumnos SET nombre = %s,correo = %s, codigo =%s, id_carrera =%s WHERE alumnos.id_alumno =%s"
            data =(name_student,email_student,code_student,id_career,id_student)
            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute(sql,data)
            connection.commit()
            row = cursor.fetchone()
            return render_template('handling/sucess/updated.html')
        else:
            return render_template('handling/error/error-update.html')
    except KeyError as e:
        print(e)
        return "Error"
    return "Error"

#Chatbot
@app.route('/get')
def get():
    userText = request.args.get('msg')
    connection = mysql.connect()
    cursor=connection.cursor()
    row = cursor.execute("SELECT respuesta FROM preguntas WHERE keyword='"+userText+"'")
    connection.commit()
    data = cursor.fetchall()
    print(row)
    if row == 1:
        result = " ".join(str(x) for x in data)
        result = result.replace("(","").replace(")","").replace("'","").replace("\\n"," ").replace("\\r"," ").replace("\\"," ")
        result = result.replace(","," ")
        print(result)
        return str(result)
    return str("No tengo esa respuesta en mi base de datos")

@app.route('/storage', methods=['POST'])
@admin_required
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
            return render_template('handling/sucess/created.html')
        else:
            return render_template('handling/error/error-save.html')
    except KeyError as e:
        print(e)
        return "Error"

@app.route('/storage-tutor', methods=['POST'])
@admin_required
def storage_tutor():
    try:
        name = request.form['name']
        email = request.form['email']
        career = request.form['career']
        connection = mysql.connect()
        cursor = connection.cursor()
        if name and email and career and request.method == 'POST':
            sql = "INSERT INTO `tutores` (`id_tutor`, `nombre`, `correo`, `id_carrera`) VALUES (NULL,%s, %s,%s);"
            data = (name, email, career)
            cursor.execute(sql,data)
            connection.commit()
            return render_template('handling/sucess/created.html')
        else:
            return render_template('handling/error/error-save.html')
    except KeyError as e:
        print(e)
        return render_template('handling/error/error-save.html')

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
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=15)
            session['studentCode'] = studentCode
            return redirect('/solar')
    return render_template('handling/error/error-login-student.html')

@app.route('/verify-master', methods=['POST'])
def verify_master():
    pwd = request.form['pwd']
    if request.method == 'POST' and pwd == '123':
        session['pwd'] = pwd
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=15)
        return redirect('/form')
    else:
        return render_template('handling/error/error-login-master.html')

@app.route('/logout-student')
def logout_student():
    session.pop('studentCode',None)
    session.permanent = False
    return redirect('/login')

@app.route('/logout-master')
def logout_master():
    session.pop('pwd',None)
    session.permanent = False
    return redirect('/master-login')

if __name__== '__main__':
    app.run(host= '0.0.0.0',port=5000, debug=True)
    #app.run(debug=True)
