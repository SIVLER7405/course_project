from flask import (
    Blueprint,
    render_template,
    current_app,
    request,
    redirect
)
from sql_provider import SQLProvider
from dbcm import work_with_db, work_with_db_update, work_with_db_insert_new_row

import os

call_app = Blueprint('call_app', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@call_app.route('/', methods=['GET', 'POST'])
def list_calls():
    if request.method == 'GET':
        services = work_with_db(current_app.config['DB_CONFIG'], provider.get('call_edit_list.sql'))
        return render_template('call_menu.html', services=services, heads=['Название услуги', 'Цена'])
    else:
        service_id = request.form['service_id']
        sql = provider.get('call_delete_service.sql', param1=service_id)
        response = work_with_db_update(current_app.config['DB_CONFIG'], sql)
        print('response=', response)
        return redirect('/call/')


@call_app.route('/edit', methods=['GET', 'POST'])
def update():
    if request.method == 'GET':
        return render_template('call_insert_new_service.html')
    else:
        part_1 = request.form.get('service_name', None)
        part_2 = request.form.get('service_cost', None)
        part_id = work_with_db_insert_new_row(current_app.config['DB_CONFIG'],
                                              provider.get('call_select_new_id.sql')) + 1

        sql = provider.get('call_insert_new_row.sql', param1=part_id, param2=part_1, param3=part_2)
        response = work_with_db_update(current_app.config['DB_CONFIG'], sql)
        print('response=', response)
        services = work_with_db(current_app.config['DB_CONFIG'], provider.get('call_edit_list.sql'))
        return render_template('call_menu.html', services=services, heads=['Название услуги', 'Цена'])