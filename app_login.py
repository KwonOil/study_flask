from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
# DB setting
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://oil:5151@100.90.191.42:3306/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'my_secret_key'

db = SQLAlchemy(app) # DB instance

login_manager = LoginManager() # LoginManager instance
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120))

    def __repr__(self):
        return '<User %r>' % self.username

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return 'Home Page'

@app.route('/protected')
@login_required
def protected():
    return f'Logged in as: {current_user.username}'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('protected'))
    return '''
        <form method="post">
            Username : <input type="text" name="username"><br>
            Password : <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/create_test_user')
def create_test_user():
    test_user = User(username='testuser', email='test@localhost.com', password='test')
    db.session.add(test_user)
    db.session.commit()
    return 'Test user created'
