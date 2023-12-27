from flask import Flask, render_template, url_for, session, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "c6e803cd18a8c528c161eb9fcf013745248506ffb540ff70thiscanbeanything"
db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    age = db.Column(db.String(4), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    def __init__(self, username, password, age, email):
        self.username = username
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()
        self.age = age
        self.email = email

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))    

    
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    if session.get('username'):
        return redirect('/upload')
    return render_template('home.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if session.get('username'):
        return redirect('/upload')
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            age = request.form['age']
            email = request.form['email']
        except:
            return render_template('login.html', loginPage=False, error='Please fill all the fields')
        try:
            new_user = User(username=username, password=password,age=age,email=email)
            db.session.add(new_user)
            db.session.commit()
        except:
            return render_template('login.html', loginPage=False, error='Username or email already exists')
        return render_template('login.html', loginPage=False, success= True)
    return render_template('login.html', loginPage=False)

@app.route('/login', methods=['GET','POST'])
def login():
    if session.get('username'):
        return redirect('/upload')
    if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session['username'] = user.username
                session['password'] = user.password
                return redirect('/upload')
            else:
                return render_template('login.html', loginPage = True, error='Invalid Username or Password')
    return render_template('login.html', loginPage=True)

@app.route('/upload', methods=['GET','POST'])
def upload():
    if session.get('username'):
        return render_template('upload.html')
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)



