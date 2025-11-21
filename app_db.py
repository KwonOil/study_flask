from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://oil:5151@100.90.191.42:3306/test'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.username

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    ### Create
    # new_user = User(username = 'John4', email = 'john4@example.com')
    # db.session.add(new_user)
    # db.session.commit()

    ### Read
    # users = User.query.all() # 모든 레코드
    # user = User.query.get(1) # id가 1인 레코드
    # filter_by : 간단한 조건, filter : 복잡한 조건
    user = User.query.filter_by(username = 'Jane3').first() # 조건에 맞는 첫 레코드
    # users = User.query.filter(User.email.endswith('@example.com')).all() # email가 @example.com로 끝나는 레코드
    # user = User.query.limit(5).all() # 5개까지 레코드

    ### Update
    # user = User.query.filter_by(username = 'John').first()
    user.email = 'Jane3@example.com'
    # users = User.query.filter_by(username = 'John').all()
    # for user in users:
    #     user.username = 'Jane'
    # User.query.filter_by(username = 'John4').update({'username':'Jane4','email': 'jane4@example.com'})
    # db.session.commit()

    ### Delete
    # user = User.query.filter_by(username = 'Jane3').first()
    db.session.delete(user)
    db.session.commit()

    return 'CRUD operations completed'