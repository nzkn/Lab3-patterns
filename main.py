from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "lab3_secret_key"

DB_PATH = 'sqlite:///D:/Politech/Patterns/lab3/course.db'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
    subject = db.Column(db.String(15))
    language = db.Column(db.String(15))
    author_id = db.Column(db.Integer)

    def __init__(self, name, subject, language, author_id):
        self.name = name
        self.subject = subject
        self.language = language
        self.author_id = author_id


@app.route('/')
def index():
    courses = Course.query.all()

    return render_template('index.html', courses=courses)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        print(request.form)
        name = request.form['name']
        subject = request.form['subject']
        language = request.form['language']
        author_id = int(request.form['author_id'])

        course = Course(name, subject, language, author_id)
        db.session.add(course)
        db.session.commit()

        flash('Course created')

        return redirect(url_for('index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        course = Course.query.get(request.form.get('id'))
        if course:
            course.name = request.form['name']
            course.subject = request.form['subject']
            course.language = request.form['language']
            course.author_id = int(request.form['author_id'])

            db.session.commit()

            flash('Course updated')

        return redirect(url_for('index'))


@app.route('/delete/<id>/', methods=['GET', 'DELETE'])
def delete(id):
    course = Course.query.get(id)

    if course:
        db.session.delete(course)
        db.session.commit()

        flash('Course deleted')

    return redirect(url_for('index'))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

