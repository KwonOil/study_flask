from flask import Blueprint    # 블루프린트

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def login():
    return '메인 페이지입니다'
