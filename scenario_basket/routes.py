from flask import (
    Blueprint,
    render_template,
    request,
    session,
    current_app,
    redirect
)
from dbcm import work_with_db, work_with_db_update
from sql_provider import SQLProvider
from .utils import add_to_basket, clear_basket
import os

basket_app = Blueprint('basket', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@basket_app.route('/', methods=['GET', 'POST'])
def list_orders():
    if request.method == 'GET':
        basket = session.get('basket', [])
        sql = provider.get('basket_list_orders.sql')
        items = work_with_db(current_app.config['DB_CONFIG'], sql)
        print(items)
        return render_template('basket_menu.html', basket=basket, items=items)
