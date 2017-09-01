import select

import socket

class Request(object):
    def __init__(self,sock,info):
        self.sock=sock
        self.info=info


    def fileno(self):
        """
        封装socket对象有fileno方法
        :return:
        """
        return self.sock.fileno()


class Custom(object):
    def __init__(self):
        self.sock_list=[]
        self.conns=[]

    def add_reqeust(self,req_info):
        """
        创建发送请求
        req_info:{'host':'www.baidu.com','port':80,'path':'/'},
        :return:
        """

        sock=socket.socket()

        sock.setblocking(False)

        try:
            sock.connect((req_info['host'],req_info['port']))
        except BlockingIOError as e:
            pass
        obj=Request(sock,req_info)
        print(obj.sock.fileno(),'------')
        self.sock_list.append(obj)
        self.conns.append(obj)

    def run(self):
        """
        开始事件循环,检测连接成功与否，数据是否返回 ？

        :return:
        """
        while 1:
            #在select的r 列表中，值必须是socket对象，对象一定要有fileno方法 ，select内部就是获取fileno方法的值,所以创建了一个 Request类，
            #并socket对象已经变成Request对象
            r,w,e=select.select(self.sock_list,self.conns,[],0.05)#e表示error,0
            #w 是否连接成功
            for obj in w:
                #这里可能是cnblogs ,可能是baidu 的字典，所以 这里需要检查obj是哪个字典 #所以用了Request类 info 就是req_info
                data="GET %s http/1.1\r\nhost:%s\r\n\r\n"%(obj.info['path'],obj.info['host'])
                obj.sock.send(data.encode('utf-8'))
                self.conns.remove(obj)#因为self.conns 检测成功的就发送数据，防止第二次进来再发送数据

            #数据返回，接收数据
            for obj in r:
                response=obj.sock.recv(8192)
                print(obj.info['host'])
                #如果这个连接成功，这个连接就移除掉。http协议的一次连接一次断开
                self.sock_list.remove(obj)


                obj.info['callback'](response)
            #所有的请求已经完成
            if not self.sock_list:
                break


def done(response):
    print(response)


url_list=[
    {'host':'www.baidu.com','port':80,'path':'/','callback':done},
    {'host':'www.bing.com','port':80,'path':'/','callback':done},
    {'host':'www.cnblogs.com','port':80,'path':'/','callback':done},
    {'host':'www.cnblogs.com','port':80,'path':'/','callback':done},
    {'host':'www.cnblogs.com','port':80,'path':'/','callback':done},
    {'host':'www.cnblogs.com','port':80,'path':'/','callback':done},
    {'host':'www.cnblogs.com','port':80,'path':'/','callback':done},
    {'host':'www.cnblogs.com','port':80,'path':'/','callback':done},
    {'host':'www.cnblogs.com','port':80,'path':'/','callback':done},
    {'host':'www.cnblogs.com','port':80,'path':'/','callback':done},
    {'host':'www.cnblogs.com','port':80,'path':'/','callback':done},
    {'host':'www.cnblogs.com','port':80,'path':'/','callback':done},
]


custom=Custom()
for item in url_list:
    custom.add_reqeust(item)
custom.run()
















