from flask import (
    Flask,
    make_response,
    request,
    abort
)

app = Flask(__name__)

@app.route('/set_cookie')
def set_cookie():
    resp = make_response('Set Cookie')
    resp.set_cookie('username', 'John')
    return resp

@app.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username','게스트')
    if username is None:
        abort(403)
    else:
        return f'Hello {username}'
    
@app.route('/secret')
def secret():
    username = request.cookies.get('username')
    if not username:
        abort(403, description="접근권한이 없습니다. 먼저 쿠키를 설정해주세요.")
    else:
        return f'Hello {username}! Welcome to the secret page!'