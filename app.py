from flask import (
    Flask,
    render_template
)
from scenario_auth.routes import auth_app
from scenario_basket.routes import basket_app
from scenario_call.routes import call_app
from scenario_user.routes import user_app

import json

app = Flask(__name__)
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(basket_app, url_prefix='/basket')
app.register_blueprint(call_app, url_prefix='/call')
app.register_blueprint(user_app, url_prefix='/user')

app.config['DB_CONFIG'] = json.load(open('config/db.json'))
app.config['SECRET_KEY'] = json.load(open('config/key.json'))


@app.route('/')
def main_menu():
    return render_template('main_menu_unauthorized.html')


@app.route('/exit')
def main_menu_exit():
    return render_template('main_menu_exit.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)

