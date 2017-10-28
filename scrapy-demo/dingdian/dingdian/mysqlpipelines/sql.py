import mysql.connector
from dingdian import settings

MYSQL_HOSTS = '127.0.0.1'
MYSQL_USER = 'admin'
MYSQL_PASSWORD = 'admin123'
MYSQL_PORT = '3306'
MYSQL_DB = 'hyjjdatabase'

cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, database=MYSQL_DB)
cur = cnx.cursor(buffered=True)

class Sql:
    @classmethod
    def insert_dd_name(cls, xs_name, xs_author, category, name_id):
        sql = 'insert into dd_name(`xs_name`, `xs_author`, `category`, `name_id`) values (%(xs_name)s, %(xs_author)s, %(category)s, %(name_id)s)'
        value = {
            'xs_name': xs_name,
            'xs_author': xs_author,
            'category': category,
            'name_id': name_id
        }
        cur.execute(sql, value)
        cnx.commit()

    @classmethod
    def select_name(cls, name_id):
        sql = 'select exists(select 1 from dd_name where name_id=%(name_id)s)'
        value = {
            'name_id' : name_id
        }

        cur.execute(sql, value)
        return cur.fetchall()[0]