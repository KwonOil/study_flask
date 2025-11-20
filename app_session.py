from flask import (
    Flask,
    session,
    abort
)

app = Flask(__name__)

app.secret_key = 'your_secret_key'

@app.route('/set_session')
def set_session():
    session['username'] = 'John'
    return '세션에 사용자 이름이 설정되었습니다!'

@app.route('/get_session')
def get_session():
    username = session.get('username')
    if username : 
        return f'사용자 이름: {username}'
    else:
        return '세션에 사용자 이름이 없습니다!'
    
@app.route('/protected')
def protected():
    if 'username' not in session:
        abort(403)
        return '이 페이지는 로그인한 사용자만 볼 수 있습니다!'
    else:
        return '로그인된 페이지입니다!'
