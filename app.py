from flask import Flask, session, request, render_template, redirect

from common import save_session, get_summary, type_to_str, startsWithList
from controller import auth, ueditor, message, comment, profile, search
from model import User, init_db
from config import logger

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.before_request
def auto_login():
    """automated login using cookie"""
    if session.get('isLogin') is None:
        username = request.cookies.get('username')
        password = request.cookies.get('password')
        if username is not None and password is not None:
            result = User.find_by_username(username)
            if len(result) == 1 and password == result[0].password:
                logger.info("用户自动登陆")
                save_session(result[0])


@app.before_request
def verify_login():
    """verify requests that need login"""
    # ignore pages don't need login
    if not startsWithList(request.path, ['/profile']):
        return
    if session.get('isLogin') is None:  # redirect to login page
        return redirect('/login?from=' + request.path)


@app.errorhandler(404)
def page_not_found(err):
    """customized 404 page"""
    logger.info("返回404页面")
    return render_template('error-404.html')


@app.route('/about')
def about():
    logger.info("用户访问ABOUT页面")
    return render_template('about.html')


# register function for Jinja
app.jinja_env.globals.update(get_summary=get_summary)
app.jinja_env.globals.update(type_to_str=type_to_str)

if __name__ == '__main__':
    app.app_context().push()
    init_db(app)

    app.register_blueprint(auth)
    app.register_blueprint(ueditor)
    app.register_blueprint(message)
    app.register_blueprint(comment)
    app.register_blueprint(profile)
    app.register_blueprint(search)

    logger.info("BBS系统启动")
    app.run(debug=True)
