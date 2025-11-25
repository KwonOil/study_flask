from flask import Flask, render_template, request, jsonify, abort
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
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Memo {self.title}>)'

# 기본 라우트
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return 'this is about page'

# DB 생성
with app.app_context():
    db.create_all()

# 메모 생성
@app.route('/memos/create', methods=['POST'])
def create_memo():
    title = request.json['title']
    content = request.json['content']

    new_memo = Memo(title=title, content=content)
    db.session.add(new_memo)
    db.session.commit()

    return jsonify({'message': 'Memo created successfully'}), 201

# 메모 조회
@app.route('/memos', methods=['GET'])
def list_momos():
    memos = Memo.query.all()
    return jsonify([{'id': memo.id, 'title': memo.title, 'content': memo.content} for memo in memos]), 200

# 메모 업데이트
@app.route('/memos/update/<int:id>',methods=['PUT'])
def update_memo(id):
    memo = Memo.query.filter_by(id=id).first()
    if memo:
        memo.title = request.json['title']
        memo.content = request.json['content']
        db.session.commit()
        return jsonify({'message': 'Memo updated successfully'}), 200
    else:
        abort(404,description="Memo not found")

# 메모 삭제
@app.route('/memos/delete/<int:id>',methods=['DELETE'])
def delete_memo(id):
    memo = Memo.query.filter_by(id=id).first()
    if memo:
        db.session.delete(memo)
        db.session.commit()
        return jsonify({'message': 'Memo deleted successfully'}), 200
    else:
        abort(404,description="Memo not found")
