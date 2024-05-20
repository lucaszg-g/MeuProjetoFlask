import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

# Configurações
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'Uma chave secreta muito secreta mesmo, duvido voce adivinhar ela'

db = SQLAlchemy(app)

UPLOAD_FOLDER = 'C:/Users/lucas/PycharmProjects/MeuProjetoFlask/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, name, password):
        self.name = name
        self.password = password


with app.app_context():
    db.create_all()


# Rotas
@app.route('/', methods=['GET', 'POST'])
def homePage():
    if 'name' in session:
        if request.method == 'POST':
            if request.files['arquivo']:
                file = request.files['arquivo']
                savePath = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(savePath)
                return render_template('homePage.html', message='Upload Successful')
            return render_template('homePage.html', error='Invalid file')
        return render_template('homePage.html')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form['usernameRegister'] != '' and request.form['passwordRegister'] != '':
            name = request.form['usernameRegister']
            password = request.form['passwordRegister']
            newUser = User(name=name, password=password)
            db.session.add(newUser)
            db.session.commit()
            return redirect(url_for('login'))
        users = User.query.all()
        return render_template('register.html', error='Invalid username or password', usuarios=users)
    users = User.query.all()
    return render_template('register.html', usuarios=users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['usernameLogin']
        password = request.form['passwordLogin']

        user = User.query.filter_by(name=name, password=password).first()

        if user and password:
            session['name'] = user.name
            return redirect(url_for('homePage'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')


@app.route('/logout')
def logout():
    if 'name' in session:
        session.pop('name', None)
        return redirect(url_for('homePage'))



if __name__ == '__main__':
    app.run(debug=True)
