from flask import (
    Blueprint,
    current_app,
    render_template,
    redirect,
    request,
    session
)
from dbcm import work_with_db
from sql_provider import SQLProvider

import os

user_app = Blueprint('user_app', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@user_app.route('/')
def user_index():
    name = session['group_name']['user_role']
    if name == 'Admin':
        return redirect("admin")
    if name == 'Employer':
        return redirect("employer")


@user_app.route('/admin', methods=['GET', 'POST'])
def render_page_admin():
    return render_template("user_menu_admin.html", name="Администратор")


@user_app.route('/employer', methods=['GET', 'POST'])
def render_page_employer():
    return render_template("user_menu_employer.html", name="Руководитель")


@user_app.route('/request_1', methods=['GET', 'POST'])
# @group_permission_decorator
def request_1():
    if request.method == 'GET':
        return render_template("request_1_form.html")
    else:
        data_year = request.form.get('data_year', None)
        if data_year is not None:
            sql = provider.get('sql_request_1.sql', param=data_year)
            result = work_with_db(current_app.config['DB_CONFIG'], sql)
            if not result:
                return render_template("user_no_data_found.html")
            context = {'schema': ["Месяц", "ID услуги", "Название услуги", "Кол-во подключений", "Кол-во отключений"], 'data': result}
            return render_template('user_menu_table_output_extended.html', context=context)
        else:
            return render_template("user_no_data_found.html")


@user_app.route('/request_2', methods=['GET', 'POST'])
# @group_permission_decorator
def request_2():
    if request.method == 'GET':
        return render_template("request_2_form.html")
    else:
        start_id = request.form.get('start_id', None)
        end_id = request.form.get('end_id', None)
        data_month = request.form.get('data_month', None)
        data_year = request.form.get('data_year', None)
        if start_id and end_id and data_month and data_year is not None:
            sql = provider.get('sql_request_2.sql', param1=start_id, param2=end_id, param3=data_month, param4=data_year)
            result = work_with_db(current_app.config['DB_CONFIG'], sql)
            if not result:
                return render_template("user_no_data_found.html")
            context = {'schema': ["ID клиента", "Имя", "Фамилия", "Отчество", "Баланс на счете"], 'data': result}
            return render_template('user_menu_table_output_extended.html', context=context)
        else:
            return render_template("user_no_data_found.html")


@user_app.route('/request_3', methods=['GET', 'POST'])
# @group_permission_decorator
def request_3():
    if request.method == 'GET':
        return render_template("request_3_form.html")
    else:
        start_date = request.form.get('start_date', None)
        end_date = request.form.get('end_date', None)
        if start_date and end_date is not None:
            sql = provider.get('sql_request_3.sql', param1=start_date, param2=end_date)
            result = work_with_db(current_app.config['DB_CONFIG'], sql)
            if not result:
                return render_template("user_no_data_found.html")
            context = {
                'schema':
                    [
                        "ID клиента",
                        "Имя",
                        "Фамилия",
                        "Отчество",
                        "Дата регистрации",
                        "Адрес",
                        "Баланс на счете",
                        "Дата последнего обновления баланса"
                    ],
                'data': result
            }
            return render_template('user_menu_table_output_super_extended.html', context=context)
        else:
            return render_template("user_no_data_found.html")

