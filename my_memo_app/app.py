from flask import Flask, render_template, request, jsonify, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

# DB 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://oil:5151@100.90.191.42:3306/my_memo_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # SQLAlchemy의 수정추적 기능 비활성화(성능상의 이유로 권장)

db = SQLAlchemy(app)

# 세션 및 로그인 설정
app.config['SECRET_KEY'] = 'my_secret_key' # 세션 및 쿠키에 대한 보안 향상을 위해 비밀키 설정

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from werkzeug.security import generate_password_hash, check_password_hash

# User 테이블 정의
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(512))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Memo 테이블 정의
class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # 사용자 참조 추가
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Memo {self.title}>)'

# 기본 라우트
@app.route('/')
def home():
    return render_template('home.html')

# 상세 페이지
@app.route('/about')
def about():
    return 'this is about page'

# DB 생성
with app.app_context():
    db.create_all()

# 메모 생성
@app.route('/memos/create', methods=['POST'])
@login_required
def create_memo():
    title = request.json['title']
    content = request.json['content']

    new_memo = Memo(user_id = current_user.id, title=title, content=content)
    db.session.add(new_memo)
    db.session.commit()

    return jsonify({'message': 'Memo created successfully'}), 201

# 메모 조회
@app.route('/memos', methods=['GET'])
@login_required
def list_memos():
    memos = Memo.query.filter_by(user_id=current_user.id).all() # 현재 로그인한 사용자의 메모만 조회
    return render_template('memos.html', memos=memos,username=current_user.username) # 사용자별 메모를 표시하는 템플릿 렌더링

# 메모 업데이트
@app.route('/memos/update/<int:id>',methods=['PUT'])
@login_required
def update_memo(id):
    memo = Memo.query.filter_by(id=id, user_id=current_user.id).first()
    if memo:
        memo.title = request.json['title']
        memo.content = request.json['content']
        db.session.commit()
        return jsonify({'message': 'Memo updated successfully'}), 200
    else:
        abort(404,description="Memo not found")

# 메모 삭제
@app.route('/memos/delete/<int:id>',methods=['DELETE'])
@login_required
def delete_memo(id):
    memo = Memo.query.filter_by(id=id,user_id=current_user.id).first()
    if memo:
        db.session.delete(memo)
        db.session.commit()
        return jsonify({'message': 'Memo deleted successfully'}), 200
    else:
        abort(404,description="Memo not found")

# 로그인
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 회원가입 라우트
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'Signup successful'}), 201
    return render_template('signup.html')

# 로그인 라우트
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return jsonify({'message': 'Login successful'}), 200
        return abort(401, description={'Invalid username or password'})
    return render_template('login.html')

# 로그아웃 라우트
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200