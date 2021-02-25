import random
import threading
import time

from Params import Const
from SQLite3Util import SQLiteUtil


class SQLServer:

    def insert_user(self, username, password):
        """
        查询用户并判断密码正确性
        :param username:
        :param password:
        :return:
        """
        sql = '''insert into t_user_info values (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        sqlite3Util = SQLiteUtil.instance('init_libu.db')
        c_time = time.localtime()
        userid = time.strftime("%Y%m%d%H%M%S", c_time) + str(random.randint(100, 999))
        c_time = time.strftime("%Y-%m-%d %H:%M:%S", c_time)
        res_val = sqlite3Util.execute_insert(sql, (userid, username, password, '', '', '0', '1', c_time, c_time))
        res_str = {Const.JSON_HEAD: {Const.JSON_CODE: Const.SUCCESS_CODE, Const.JSON_MSG: Const.SUCCESS_MSG},
                       Const.JSON_BODY: {}}
        return res_str

    def select_user(self, username, password):
        """
        查询用户并判断密码正确性
        :param username:
        :param password:
        :return:
        """
        sql = '''select t_userid, t_password from t_user_info where t_username = ?'''
        sqlite3Util = SQLiteUtil.instance('init_libu.db')
        res_val = sqlite3Util.execute_select(sql, (username,))
        # print(res_val)
        if password == res_val[0]['t_password']:
            res_str = {Const.JSON_HEAD: {Const.JSON_CODE: Const.SUCCESS_CODE, Const.JSON_MSG: Const.SUCCESS_MSG},
                       Const.JSON_BODY: {'p_userid': res_val[0]['t_userid']}}
        else:
            res_str = {Const.JSON_HEAD: {Const.JSON_CODE: Const.ERROR_0010, Const.JSON_MSG: Const.MSG_0010},
                       Const.JSON_BODY: {}}
        return res_str




def task(arg):
    obj = SQLServer()
    res = obj.insert_user('admin', 'admin')
    # print('1', obj)
    print(res)


# task(0)

# for i in range(10):
#     t = threading.Thread(target=task, args=[i, ])
#     t.start()
