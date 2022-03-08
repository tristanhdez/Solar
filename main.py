from flask import Flask
from flask import render_template, Response, request, session
from datetime import timedelta
from flaskext.mysql import MySQL
from werkzeug.utils import redirect
from functools import wraps
from flask_mail import Mail, Message
from io import TextIOWrapper
import secrets
import io
import xlwt
import re
import queue
import random
import csv


app = Flask(__name__)
#With os
#os.random(24)
app.config['SECRET_KEY'] = 'secret-key:)'
mysql= MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='Password123*'
app.config['MYSQL_DATABASE_DB']='tutorias'
mysql.init_app(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'holasoysolarelbot@gmail.com'
app.config['MAIL_PASSWORD'] = 'zyyywjwgqtbbtswm'
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
q = queue.Queue()


answers = [
    "¡Por supuesto!😄\n",
    "Of course!🤪\n",
    "E-N S-E-G-U-I-D-A...🤖\n",
    "'Yes' en Inglés 🧾(Jobs😉)\n",
    "I'm coming!👀\n",
    "¡Claro!🤓\n",
    "🧐¡Enseguida!\n",
    "Buscando...🔍\t ¡Aquí está!🤓\n",
    "Searching...🔍\t Check it out!🤓\n",
]


without_answers=[
    "No tengo esa información😰\n",
    "No lo encuentro en mi base de datos😱\n",
    "🤨I don't understand you\n",
    "Hmmm, I don't know😧\n You could send your question below📫",
    "No entiendo😖\n Puedes mandar correo con tu pregunta y pronto estará aquí🤓",
    "Uy, no tengo respuesta para ello😶\n ¡Sugiere la pregunta aquí abajo!👇",
    "No cuento con esa información😓\n Si quieres ver tu respuesta, ¡Sugiere una pregunta!🤓",
    "No te lo vengo manejando, joven🤠\n ¡Deberías sugerir la pregunta!",
]

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'pwd' in session:
            return f(*args, **kwargs)
        else:
            return render_template('handling/error/expired-session.html')
    return wrap

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'studentCode' in session:
            return f(*args, **kwargs)
        else:
           return render_template('handling/error/expired-session.html')
    return wrap


@app.route('/solar')
@app.route('/chatbot')
@login_required
def index():
    return render_template('student/index.html')

@app.route('/login')
def login():
    return render_template('student/login.html')

@app.route('/keywords')
@login_required
def keywords():
    return render_template('student/keywords.html')

@app.route('/')
def home():
        return render_template('home.html')

@app.route('/select')
def select():
        return render_template('select.html')

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

@app.route('/new-student')
@admin_required
def new_student():
    return render_template('tutor/new-student.html')

@app.route('/new-tutor')
@admin_required
def new_tutor():
    return render_template('tutor/new-tutor.html')


@app.route('/upload-questions')
@admin_required
def upload():
    return render_template('tutor/upload-questions.html')

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
''''
@app.route('/error-form')
def error_form():
    return render_template('handling/error/error-form.html')
'''

@app.route('/download/report/excel/tutor-and-student')
def download_report():
    sql = "SELECT tutores.id_tutor, tutores.nombre, tutores.correo,carreras.id_carrera, carreras.nombre AS carrera, alumnos.id_alumno, alumnos.nombre AS alumnos FROM alumnos INNER JOIN carreras ON alumnos.id_carrera = carreras.id_carrera INNER JOIN tutores ON alumnos.id_tutor = tutores.id_tutor";
    connection= mysql.connect()
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    connection.commit()

    #output in bytes
    output = io.BytesIO()
    #create WorkBook object
    workbook = xlwt.Workbook()
    #add a sheet
    sh = workbook.add_sheet('Tutor and Student Report')

    #add headers
    sh.write(0, 0, 'Id del Tutor')
    sh.write(0, 1, 'Nombre del tutor')
    sh.write(0, 2, 'Correo de Tutor')
    sh.write(0, 3, 'Id de la carrera')
    sh.write(0, 4, 'Carrera')
    sh.write(0, 5, 'Id del alumno')
    sh.write(0, 6, 'Nombre de alumno')
    idx = 0
    for row in data:
        sh.write(idx+1, 0, str(row[0]))
        sh.write(idx+1, 1, row[1])
        sh.write(idx+1, 2, row[2])
        sh.write(idx+1, 3, str(row[3]))
        sh.write(idx+1, 4, row[4])
        sh.write(idx+1, 5, str(row[5]))
        sh.write(idx+1, 6, row[6])
        idx += 1

    workbook.save(output)
    output.seek(0)

    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=Tutor_&_Estudiante.xls"})


@app.route('/download/report/excel/tutors')
def download_report_tutors():
    sql = "SELECT tutores.id_tutor, tutores.nombre, tutores.correo, carreras.id_carrera, carreras.nombre AS carreras FROM tutores INNER JOIN carreras ON tutores.id_carrera = carreras.id_carrera;";
    connection= mysql.connect()
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    connection.commit()

    #output in bytes
    output = io.BytesIO()
    #create WorkBook object
    workbook = xlwt.Workbook()
    #add a sheet
    sh = workbook.add_sheet('Tutors Report')

    #add headers
    sh.write(0, 0, 'Nombre')
    sh.write(0, 1, 'Correo')
    sh.write(0, 2, 'Carrera')
    idx = 0
    for row in data:
        sh.write(idx+1, 0, row[1])
        sh.write(idx+1, 1, row[2])
        sh.write(idx+1, 2, row[4])
        idx += 1
    workbook.save(output)
    output.seek(0)
    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=Tutores.xls"})

@app.route('/download/report/excel/students')
def download_report_students():
    sql = "SELECT alumnos.id_alumno, alumnos.nombre, alumnos.correo, alumnos.codigo, carreras.id_carrera, carreras.nombre AS carreras FROM alumnos INNER JOIN carreras ON alumnos.id_carrera = carreras.id_carrera;";
    connection= mysql.connect()
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    connection.commit()

    #output in bytes
    output = io.BytesIO()
    #create WorkBook object
    workbook = xlwt.Workbook()
    #add a sheet
    sh = workbook.add_sheet('Students Report')

    #add headers
    sh.write(0, 0, 'Nombre')
    sh.write(0, 1, 'Correo')
    sh.write(0, 2, 'Código')
    sh.write(0, 3, 'Carrera')
    idx = 0
    for row in data:
        sh.write(idx+1, 0, row[1])
        sh.write(idx+1, 1, row[2])
        sh.write(idx+1, 2, row[3])
        sh.write(idx+1, 3, row[5])
        idx += 1
    workbook.save(output)
    output.seek(0)
    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=Estudiantes.xls"})


@app.route('/download/report/excel/questions')
def download_report_questions():
    sql = "SELECT preguntas.id_pregunta, preguntas.pregunta, preguntas.respuesta, keyword, etapas.etapa FROM preguntas JOIN etapas ON preguntas.id_etapa = etapas.id_etapa";
    connection= mysql.connect()
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    connection.commit()
    #output in bytes
    output = io.BytesIO()
    #create WorkBook object
    workbook = xlwt.Workbook()
    #add a sheet
    sh = workbook.add_sheet('Questions Report Solar')
    #add headers
    sh.write(0, 0, 'Pregunta')
    sh.write(0, 1, 'Respuesta')
    sh.write(0, 2, 'Palabra Clave')
    sh.write(0, 3, 'Etapa')
    idx = 0
    for row in data:
        sh.write(idx+1, 0, row[1])
        sh.write(idx+1, 1, row[2])
        sh.write(idx+1, 2, row[3])
        sh.write(idx+1, 3, row[4])
        idx += 1
    workbook.save(output)
    output.seek(0)
    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=Preguntas_Solar.xls"})

@app.route('/importing/questions', methods=['GET', 'POST'])
def importing_questions():
    if request.method == 'POST':
        csv_file = request.files['csvfile']
        csv_file = TextIOWrapper(csv_file, encoding='utf-8')
        csv_reader = csv.reader(csv_file)
        connection = mysql.connect()
        cursor = connection.cursor()
        sql = "INSERT INTO `preguntas` (`id_pregunta`, `pregunta`, `respuesta`, `keyword`, `id_etapa`) VALUES (NULL, %s, %s, %s, %s);"
        for row in csv_reader:
            cursor.execute(sql,row)
            connection.commit()
        return "ok"
    return "no"

@app.route("/sending-email", methods=['POST','GET'])
@login_required
def sending_email():
    body = request.form['body']
    name = request.form['name']
    if request.method == "POST" and body and name:
        msg = Message("¡Nueva Pregunta Sugerida!", sender= 'holasoysolarelbot@gmail.com',recipients= ["holasoysolarelbot@gmail.com"])
        msg.body = "¡Hola, Administrador!\n¡Un alumno ha enviado una nueva sugerencia!\nNombre: "+name+"\nPregunta: "+request.form.get("body")+"\n¡Chécalo aquí!:"+"http://127.0.0.1:5000/emails"
        with app.open_resource("static/images/character/new-suggest.jpeg") as fp:
            msg.attach("new-suggest.jpeg", "image/jpeg", fp.read())
        mail.send(msg)
        connection = mysql.connect()
        cursor = connection.cursor()
        sql = "INSERT INTO `sugerencias` (`id_email`, `name`, `message`, `status`) VALUES (NULL, %s, %s,'Pendiente');"
        data = (name,body)
        cursor.execute(sql,data)
        connection.commit()
        return render_template("student/result-email.html", result="¡Sugerencia Enviada!")
    else:
       return render_template("student/result-email.html", result="Error, intenta nuevamente")

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
        return render_template('handling/error/error-form.html')

@app.route('/emails')
@admin_required
def emails():
    try:
        sql = "SELECT * FROM sugerencias";
        connection= mysql.connect()
        cursor = connection.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        connection.commit()
        return render_template('tutor/emails.html', data=data)
    except KeyError as e:
        print(e)
        return render_template('handling/error/error-form.html')

@app.route('/validate-suggest/<int:id>/')
@admin_required
def validate_suggest(id):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sugerencias WHERE id_email=%s",(id))
        data = cursor.fetchall()
        connection.commit()
        return render_template('tutor/edit-suggest.html', data = data)
    except KeyError as e:
        print(e)
        return render_template('handling/error/error-form.html')

@app.route('/storing-suggest', methods=['POST'])
@admin_required
def storing_suggest():
    try:
        id_email = request.form['id_email']
        name = request.form['name']
        suggest = request.form['suggest']
        question = request.form['question']
        answer = request.form['answer']
        stage = request.form['stage']
        keyword = request.form['keyword']
        status = request.form['status']
        connection = mysql.connect()
        cursor = connection.cursor()
        if name and question and answer and suggest and status and id_email and stage and keyword and status and request.method == 'POST':
            sql = "INSERT INTO `preguntas` (`id_pregunta`, `pregunta`, `respuesta`, `keyword`, `id_etapa`) VALUES (NULL, %s, %s, %s, %s);"
            data = (question, answer, keyword, stage)
            cursor.execute(sql,data)
            connection.commit()
            connection.close()
        else:
            return render_template('handling/error/error-save.html')
        if id_email:
            connection = mysql.connect()
            cursor = connection.cursor()
            sql1 = "UPDATE sugerencias SET status = %s WHERE sugerencias.id_email =%s"
            data =(status,id_email)
            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute(sql1,data)
            connection.commit()
            connection.close()
        else:
            return render_template('handling/error/error-save.html')
        return render_template('handling/sucess/created.html')
    except KeyError as e:
        print(e)
        return render_template('handling/error/error-save.html')


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
        return render_template('handling/error/error-form.html')

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
        return redirect('handling/error/error-form.html')
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
        return redirect('handling/error/error-form.html')
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
        return redirect('handling/error/error-form.html')
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
            return redirect('handling/error/error-form.html')
    except KeyError as e:
        print(e)
        return redirect('handling/error/error-form.html')


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
    if userText == "hola":
        return str("¡Hola, soy Solar!☀️🤖\n Estoy a tus órdenes😊")
    if re.match("^[0-9]{9}$", userText):
        connection = mysql.connect()
        cursor=connection.cursor()
        row = cursor.execute("SELECT tutores.nombre from tutores join alumnos on tutores.id_tutor = alumnos.id_tutor where alumnos.codigo ='"+userText+"'")
        connection.commit()
        data = cursor.fetchall()
        if row == 1:
            result = " ".join(str(x) for x in data)
            result = result.replace("(","").replace(")","").replace("'","").replace("\\n"," ").replace("\\r"," ").replace("\\"," ")
            result = result.replace(","," ")
            return "Claro, tu tutor/tutora es: "+result
        else:
            return "No encontramos tu tutor, intenta nuevamente"
    connection = mysql.connect()
    cursor=connection.cursor()
    row = cursor.execute("SELECT respuesta FROM preguntas WHERE keyword='"+userText+"'")
    connection.commit()
    data = cursor.fetchall()
    print(data)
    if row == 1:
        result = " ".join(str(x) for x in data)
        result = result.replace("(","").replace(")","").replace("'","").replace("\\n"," ").replace("\\r"," ").replace("\\"," ")
        result = result.replace(","," ")
        print(result)
        answer = random.choice(answers)
        return answer+result
    withoutanswer = random.choice(without_answers)
    return withoutanswer

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

@app.route('/storage-student', methods=['POST'])
@admin_required
def storage_student():
    try:
        name = request.form['name']
        email = request.form['email']
        career = request.form['career']
        code = request.form['code']
        tutor = request.form['tutor']
        connection = mysql.connect()
        cursor = connection.cursor()
        if name and email and career and code and tutor and request.method == 'POST':
            sql = "INSERT INTO `alumnos` (`id_alumno`, `nombre`, `correo`, `codigo`, `id_carrera`, `id_tutor`) VALUES (NULL, %s, %s, %s, %s, %s);;"
            data = (name, email, code, career, tutor)
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
            connection = mysql.connect()
            cursor=connection.cursor()
            cursor.execute("SELECT nombre FROM alumnos WHERE codigo='"+studentCode+"'")
            connection.commit()
            name = cursor.fetchall()
            value = " ".join(str(x) for x in name)
            value = value.replace("(","").replace(")","").replace(","," ").replace("'","")
            session['studentCode'] = studentCode
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=120)
            return redirect('/solar')
    return render_template('handling/error/error-login-student.html')

@app.route('/verify-master', methods=['POST'])
def verify_master():
    pwd = request.form['pwd']
    if request.method == 'POST' and pwd == '123':
        session['pwd'] = pwd
        key = secrets.token_urlsafe(5)
        q.put(key)
        print(q.queue)
        msg = Message("🔑¡Llave Secreta!🔑", sender= 'holasoysolarelbot@gmail.com',recipients= ["holasoysolarelbot@gmail.com"])
        msg.body = "¡Hola, Administrador!👋\n ¡Para poder proceder necesitamos la palabra clave!\n"+"Key:"+key+"\n¡Chécalo!👀"
        mail.send(msg)
        return render_template('tutor/verify-key.html')
    else:
        return render_template('handling/error/error-login-master.html')

@app.route('/request-code', methods=['POST'])
def request_code():
    original_key = q.get(1)
    print(q.queue)
    email_key = request.form['key']
    if original_key == email_key:
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=120)
        q.queue.clear()
        print(q.queue)
        del original_key, email_key
        return redirect('/form')
    else:
        q.queue.clear()
        del original_key, email_key
        return render_template('handling/error/error-key.html')


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
