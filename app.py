from flask import Flask, render_template, request, redirect, url_for
from flask_mysql import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'task_manager'

mysql = MySQL(app)

# Task Model
class TaskForm(FlaskForm):
    task = StringField('Task', validators=[InputRequired()])

# Routes
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tasks')
    tasks = cur.fetchall()
    cur.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    form = TaskForm(request.form)
    if form.validate():
        task = form.task.data
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO tasks (task) VALUES (%s)', (task,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template('index.html', form=form)

@app.route('/delete/<int:id>')
def delete_task(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM tasks WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
