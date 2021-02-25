# coding:utf-8
# 处理数据库工具类
# 单例模式
# 2021/2/20

import sqlite3
import queue
import threading
import time


class SQLiteUtil(object):
    # 加锁， 多线程时串行
    _instance_lock = threading.Lock()
    __queue_conn = queue.Queue(maxsize=1)
    __path = None

    def __init__(self, path):
        self.__path = path
        print('path:', self.__path)
        self.__create_conn()

    def __create_conn(self):
        """
        建立连接并放到队列中
        :return:
        """
        conn = sqlite3.connect(self.__path, check_same_thread=False)
        self.__queue_conn.put(conn)

    def __close(self, cursor, conn):
        """
        关闭连接
        :param cursor:
        :param conn:
        :return:
        """
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
            self.__create_conn()

    def execute_select(self, sql, params):
        """
        查詢sql
        :param sql:
        :param params:
        :return:
        """
        conn = self.__queue_conn.get()
        cursor = conn.cursor()
        value, records = None, None
        try:
            if not params is None:
                records = cursor.execute(sql, params).fetchall()
            else:
                records = cursor.execute(sql).fetchall()
            field = [i[0] for i in cursor.description]
            # print('field', field)
            value = [dict(zip(field, i)) for i in records]
            # print('records', records)
            # print('value', value)
        finally:
            self.__close(cursor, conn)
        return value

    def execute_insert(self, sql, params):
        """
        插入sql
        :param sql:
        :param params:
        :return:
        """
        conn = self.__queue_conn.get()
        cursor = conn.cursor()
        value, records = None, None
        try:
            if not params is None:
                records = cursor.execute(sql, params).fetchall()
            else:
                records = cursor.execute(sql).fetchall()
            print('records', records)
        finally:
            self.__close(cursor, conn)
        return value

    def execute_script(self, sql):
        """
        执行多条sql, 分号隔开
        :param sql:
        :return:
        """
        conn = self.__queue_conn.get()
        cursor = conn.cursor()
        try:
            cursor.executescript(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            self.__close(cursor, conn)

    def execute_update(self, sql, params):
        """
        修改单一sql, 返回修改数据条数
        :param sql:
        :param params:
        :return: 修改数据条数
        """
        return self.execute_update_many([sql], [params])

    def execute_update_many(self, sql_list, params_list):
        """
        批量修改sql, 返回修改数据条数
        :param sql_list:
        :param params_list:
        :return: 修改数据条数
        """
        conn = self.__queue_conn.get()
        cursor = conn.cursor()
        count = 0
        try:
            for index in range(len(sql_list)):
                sql = sql_list[index]
                params = params_list[index]
                if not params is None:
                    count += cursor.execute(sql, params).rowcount
                else:
                    count += cursor.execute(sql).rowcount
                    conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            self.__close(cursor, conn)
        return count

    # 如果使用__new__方法实现单例会多次执行(__init__/__create_conn)导致程序挂起
    # def __new__(cls, *args, **kwargs):
    @classmethod
    def instance(cls, *args, **kwargs):
        # 判断是否为单例, 如果是单例没必要拿锁
        if not hasattr(SQLiteUtil, "_instance"):
            with SQLiteUtil._instance_lock:
                # 防止多线程时其他线程多次拿实例
                if not hasattr(SQLiteUtil, "_instance"):
                    SQLiteUtil._instance = SQLiteUtil(*args, **kwargs)
        return SQLiteUtil._instance

'''
example:

one = SQLiteUtil('xxx.sqlite')

rst = one.execute_query('select * from website', None)
for line in rst:
print(line.get('id'), line.get('url'), line.get('content'))


print(one.execute_update('update website set content = \'2222222\' where id = ?', ('1',)))
print(one.execute_update('update website set content = \'2222222\' where id = \'1\'', None))


print('update many')
count = one.execute_update_many(
[
'update website set content = \'一\' where id = \'1\'',
'update website set content = \'二\' where id = \'2\'',
'update website set content = 1 where id = \'3\''
],
[None, None, None]
)
print('count:', count)
'''


def task(arg):
    obj = SQLiteUtil.instance('init_libu.db')
    # obj = SQLiteUtil('init_libu.db')
    sql = '''select t_password from t_user_info where t_username = ?'''
    res_val = obj.execute_oneSQL(sql, ('admin',))
    print(res_val)
    print(arg, obj)


if __name__ == '__main__':
    # 测试多线程实例情况
    for i in range(10):
        # time.sleep(2)
        t = threading.Thread(target=task, args=[i, ])
        t.start()

