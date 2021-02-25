# 服务发布

from aiohttp import web
# import SQLServer

from Params import Const
from SQLServer import SQLServer


async def test(request):
    name = request.match_info.get('name', '默认值')
    text = name + ', 是无效的url'
    return web.Response(text=text)


async def register(request):
    """
    注册用户
    :param request:
    :return:
    """
    req = dict(request.headers)
    username = req['username']
    password = req['password']
    print(username, password)
    res_str = {Const.JSON_HEAD: {Const.JSON_CODE: Const.ERROR_9999, Const.JSON_MSG: Const.MSG_9999},
               Const.JSON_BODY: {}}
    if not username and not password:
        res_str[Const.JSON_HEAD][Const.JSON_CODE] = Const.ERROR_0001
        res_str[Const.JSON_HEAD][Const.JSON_MSG] = Const.MSG_0001
    else:
        sqlServer = SQLServer()
        res_str = sqlServer.insert_user(username, password)
    return web.Response(text=str(res_str))


async def login(request: web.Request):
    """
    登陆
    :param request:
    :return:
    """
    req = dict(request.headers)
    username = req['username']
    password = req['password']
    print(username, password)
    res_str = {Const.JSON_HEAD: {Const.JSON_CODE: Const.ERROR_9999, Const.JSON_MSG: Const.MSG_9999},
               Const.JSON_BODY: {}}
    # print(username, password)
    if not username and not password:
        res_str[Const.JSON_HEAD][Const.JSON_CODE] = Const.ERROR_0001
        res_str[Const.JSON_HEAD][Const.JSON_MSG] = Const.MSG_0001
    else:
        sqlServer = SQLServer()
        res_str = sqlServer.select_user(username, password)
    print(str(res_str))
    return web.Response(text=str(res_str))


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([web.get('/', test),
                    web.post('/register', register),
                    web.post('/login', login, expect_handler=web.Request.json),
                    web.post('/{name}', test)])
    web.run_app(app, host='127.0.0.1', port=8888)
