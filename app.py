from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)

app.config["SECRET_KEY"] = "user@321"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///api.sqlite3"

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        users = Users.query.all()
        for user in users:
            if request.form['username'] == user.username:
                if bcrypt.checkpw(request.form['password'].encode('ASCII'), user.password):
                    name = user.username.capitalize()
                    return render_template('index.html', name = name)
                    
    return render_template('login.html')

@app.route('/signin', methods=['GET','POST'])
def signin():    
    if request.method == 'POST':
        if not request.form['username'] or not request.form['password']:
            print('Please, enter all required data.')
        else:
            hashed = bcrypt.hashpw(request.form['password'].encode('ASCII'), bcrypt.gensalt(14))
            user = Users(request.form['username'], hashed)
            db.session.add(user)
            db.session.commit()
            print('Successfuly created!')
            
            return redirect(url_for('login'))
         
    return render_template('signin.html')

if __name__ == '__main__':    
    app.run()
    