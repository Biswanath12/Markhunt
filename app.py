from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/Markhunt/user.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


# Uncomment the line below during initial setup to create tables
# create_tables()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    new_user = User(username=username, password=password, email=email)

    try:
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    except IntegrityError:
        db.session.rollback()
        return 'Username or email already exists. Please choose another.'


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # Handle login form submission
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            # Redirect to home page and pass the username in the URL
            return redirect(url_for('home', username=user.username))
        else:
            return 'Invalid username or password.'

    # If the request method is GET, render the login form
    return render_template('login.html')


@app.route('/home/<username>')
def home(username):
    return render_template('home.html', username_from_flask=username)


@app.route('/contact.html')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
