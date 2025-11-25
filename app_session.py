from flask import ( # 웹 애플리케이션과 세션 관리
    Flask,
    request,
    redirect,
    url_for,
    session
)
from flask_sqlalchemy import SQLAlchemy # ORM을 위한 플라스크 확장
from flask_login import ( # 사용자 인증 관리
    LoginManager,
    login_required,
    login_user,
    logout_user,
    UserMixin,
    current_user
)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://oil:5151@100.90.191.42:3306/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'my_secret_key'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class UserTable(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120))

    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return UserTable.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    user_id = session.get('user_id')
    if user_id:
        user = UserTable.query.get(user_id)
        return f'Logged in as: {user.username}'
    return 'Not logged in'

@app.route('/protected')
@login_required
def protected():
    return f'Logged in as: {current_user.username}'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = UserTable.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            session['user_id'] = user.id
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
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/create_test_user')
def create_test_user():
    test_user = UserTable(username='test', email='test@localhost.com', password='test')
    db.session.add(test_user)
    db.session.commit()
    return 'Test user created'
