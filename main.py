from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



##CREATE TABLE IN DB
class Task(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_to_complete = db.Column(db.String(250), unique=True)
    date = db.Column(db.DateTime)
    favourite = db.Column(db.Boolean)
    completed = db.Column(db.Boolean)
#Line below only required once, when creating DB. 
# db.create_all()


@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template("index.html", all_tasks=tasks)

@app.route('/fave/<int:task_id>', methods=['GET','POST'])
def fave(task_id):
    task = Task.query.get(task_id)
    task.favourite = not task.favourite
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<int:task_id>', methods=['GET','POST'])
def delete_task(task_id):
    task_to_delete = Task.query.get(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/complete/<int:task_id>', methods=['GET','POST'])
def complete(task_id):
    task_completed = Task.query.get(task_id)
    task_completed.completed = True
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        task = Task(
            task_to_complete=request.form.get('task'),
            completed=False
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
