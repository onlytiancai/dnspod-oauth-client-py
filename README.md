## DNSPod oAuth Client SDK for python

本项目提供了DNSPoc oAuth客户端的Python SDK，并有一个web.py使用该SDK的例子。

### 如何测试

1. 去[DNSPod](https://dnspod.cn)申请oAuth相关的client id和client key，并在appmain.py里配置好。
1. 在src目录下运行python appmain.py 0.0.0.0:8888
1. 浏览器打开http://localhost:8888，就可以使用DNSPod账户登录并获取到用户昵称了。

