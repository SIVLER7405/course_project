from pymysql import connect
from pymysql.err import InterfaceError
from pymysql.err import OperationalError


class UserDataBase:

    def __init__(self, config):
        self.config = config

    def __enter__(self):
        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except OperationalError as err:
            if err.args[0] == 1045:
                print('Неверный логин и/или имя хоста и/или пароль')
                return None
            if err.args[0] == 1049:
                print('Неверное название базы данных')
                return None
            if err.args[0] == 2003:
                print('Неверно введен порт или хост для подключения к серверу')
                return None
        except UnicodeEncodeError as err:
            print(err, ': Были введены символы на русском языке')
            return None
        except InterfaceError as err:
            print(err)
            return err

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            if exc_val.args[0] == 'cur':
                print('Курсор не создан')
            elif exc_val.args[0] == 1064:
                print('Синтаксическая ошибка в запросе!')
            elif exc_val.args[0] == 1146:
                print('Ошибка в запросе! Такой таблицы не существует')
            elif exc_val.args[0] == 1054:
                print('Ошибка в запросе! Такого поля не существует')
            return True
        else:
            self.conn.commit()
            self.conn.close()
            self.cursor.close()
            return True


def work_with_db(config, sql):
    result = []
    with UserDataBase(config) as cursor:
        if cursor is None:
            raise ValueError('cur')
        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result.append(dict(zip(schema, row)))
        return result


def work_with_db_update(config, sql):
    with UserDataBase(config) as cursor:
        return cursor.execute(sql)


def work_with_db_insert_new_row(config, sql):
    with UserDataBase(config) as cursor:
        cursor.execute(sql)
        return cursor.fetchone()[0]
