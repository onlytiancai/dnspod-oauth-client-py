# -*- coding: utf-8 -*-

import web
import json
from oauth import OAuth

# 以下三个配置项需要去DNSPod申请
DNSPOD_CLIENT_ID = '10020'
DNSPOD_CLIENT_SECRET = '****'
DNSPOD_CALLBACK = 'http://172.4.2.20:8888/dnspodcallback'

dnspodOAuth = OAuth(
    name='dnspod',
    client_id=DNSPOD_CLIENT_ID,
    client_secret=DNSPOD_CLIENT_SECRET,
    base_url='https://www.dnspod.cn/Api/',
    access_token_url='https://www.dnspod.cn/OAuth/Access.Token',
    authorize_url='https://www.dnspod.cn/OAuth/Authorize')


class index(object):
    '''显示登陆链接'''
    def GET(self):
        web.header('Content-Type', 'text/html; charset=utf-8', unique=True)
        return "<a href='/dnspodlogin'>使用DNSPod登陆</a>"


class dnspodlogin(object):
    '''生成授权链接并重定向过去'''
    def GET(self):
        url = dnspodOAuth.get_authorize_url(response_type='code',
                                            redirect_uri=DNSPOD_CALLBACK,
                                            )
        return web.redirect(url)


class dnspodcallback(object):
    def get_access_token(self, code):
        '''获取access token'''
        result = dnspodOAuth.get_access_token('GET',
                                              code=code,
                                              grant_type='authorization_code',
                                              redirect_uri=DNSPOD_CALLBACK)
        result = json.loads(result)
        return result['access_token']

    def get_nickname(self, access_token):
        '''使用access_token调用DNSPod API获取用户昵称'''
        api_result = dnspodOAuth.request('POST', 'User.Detail', access_token=access_token, format='json')
        api_result = json.loads(api_result)
        result = api_result['info']['user']['nick']
        if result is None:
            result = api_result['info']['user']['real_name']
        if result is None:
            result = 'DNSPod用户'
        return result

    def GET(self):
        web.header('Content-Type', 'text/html; charset=utf-8', unique=True)
        code = web.input().code

        if code:
            access_token = self.get_access_token(code)
            nickname = self.get_nickname(access_token)
            return "欢迎您%s" % nickname.encode('utf-8')


urls = ["/", "index",
        "/dnspodlogin", "dnspodlogin",
        "/dnspodcallback", "dnspodcallback",
        ]

app = web.application(urls, globals())

if __name__ == '__main__':
    import logging
    logging.getLogger().setLevel(logging.NOTSET)
    app.run()
