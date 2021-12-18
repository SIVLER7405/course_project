from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    request,
    session
)
from dbcm import work_with_db
from sql_provider import SQLProvider

import os

auth_app = Blueprint('auth_app', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@auth_app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('auth_menu.html')
    else:
        login = request.form.get('login', None)
        password = request.form.get('password', None)

        if login is not None and password is not None:
            sql = provider.get('auth.sql', gen1=login, gen2=password)
            result = work_with_db(current_app.config['DB_CONFIG'], sql)
            if not result:
                return render_template("auth_invalid.html")
            session['group_name'] = result[0]
            name = session['group_name']['user_role']
            if name == 'Admin':
                return redirect("admin")
            if name == 'Employer':
                return redirect("employer")
            if name == 'Employee':
                return redirect("employee")


@auth_app.route('/admin', methods=['GET', 'POST'])
def render_page_admin():
    return render_template("main_menu_admin.html", name="Администратор")


@auth_app.route('/employer', methods=['GET', 'POST'])
def render_page_employer():
    return render_template("main_menu_employer.html", name="Руководитель")


@auth_app.route('/employee', methods=['GET', 'POST'])
def render_page_employee():
    return render_template("main_menu_employee.html", name="Сотрудник")

