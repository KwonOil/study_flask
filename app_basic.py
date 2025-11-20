from flask import (Flask,
                   request, # 요청
                   make_response, # 응답
                   jsonify, # 딕셔너리를 json형식으로 변환
                   url_for,  # URL 빌더
                   render_template,  # HTML파일 전달
                   send_from_directory  # 파일 전달
)
app = Flask(__name__)

# 기본
@app.route('/')
def home():
    return render_template('index.html')

# 변수를 입력받아 사용
@app.route('/user/<username>')
def show_user_profile(username):
    return f'User {username}'

@app.route('/post/<year>/<month>/<day>')
def show_post(year, month, day):
    return f'Post for {year}/{month}/{day}'

# 요청 처리
@app.route('/query')
def query_example():
    language = request.args.get('language')
    return f'Requested language : {language}'

# 응답 처리
@app.route('/json')
def json_example():
    return jsonify({"message":"Hello,World"})

# make_response
@app.route('/response')
def response_example():
    resp = make_response("Hello with header", 200)
    resp.headers['Custom-Header'] = 'custom-value'
    return resp

# HTTP 메서드 사용
@app.route('/login', methods = ['get','post'])
def login():
    if request.method == 'POST':
        return 'Logging in...'
    else :
        return 'LoginForm'

# render_template 기본
@app.route('/hello/<name>')
def hello_name(name):
    return render_template('hello.html',name = name)

@app.route('/fruits')
def show_fruits():
    fruits = ['apple', 'banana', 'cherry']
    return render_template('fruits_list.html', fruits = fruits)

# macro 이용
@app.route('/messages')
def show_messages():
    return render_template('messages.html')

# extends 이용
@app.route('/about')
def about_page():
    return render_template('about.html')

# send_from_directory 이용
@app.route('/image')
def get_image():
    return send_from_directory(app.static_folder,'image.jpg')




if __name__ == '__main__':
    app.run(debug=True)