import socket
import sys
import threading
import json
from googletrans import Translator
import re

dict_repertoire = '/root/dict_FrToCn/24s_translation/24s/dict_24s/'


def translate(data):
    data = ''.join(data)
    translator = Translator()
    trans_data = translator.translate(data, src='fr', dest='zh-cn')
    return trans_data.text

def data_pretraiter(data):

    data_fr = re.split(' ',data.lower())
    data_garde = ''
    try:
        with open(dict_repertoire+'motGarde_dict.json', encoding='utf-8') as motGarde_dict:
            motGarde_dict = json.load(motGarde_dict)
            new_data_fr = []
            for each in data_fr:
                have = True
                for every in motGarde_dict:
                    if each == every:
                        data_garde = each
                        have = False
                if have:
                    new_data_fr.append(each)
            return ' '.join(new_data_fr),data_garde
    except Exception:
        return ' '.join(data_fr), data_garde

def transDef(word,dict):
    dict_name = dict
    dict_path = dict_repertoire + dict_name
    with open(dict_path, encoding='utf-8') as accessoires_dict:
        data = json.load(accessoires_dict)
        emptyDict = {}
        frWord = word.lower()
        for each in data:
            emptyDict[each['wordFr']] = each['wordCn']
        try:
            return (emptyDict[frWord])
        except Exception as err:
            if len(frWord.split(' ')) > 3:
                col = []
                data_apresTraitement, mot_garde = data_pretraiter(frWord)
                return (mot_garde + translate(data_apresTraitement))
            else:
                frWord = frWord.split(' ')[0]
                return (emptyDict[frWord])


def main():
    # 创建服务器套接字
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取本地主机名称
    host = socket.gethostname()
    # 设置一个端口
    port = 12345
    # 将套接字与本地主机和端口绑定
    serversocket.bind((host, port))
    # 设置监听最大连接数
    serversocket.listen(5)
    # 获取本地服务器的连接信息
    myaddr = serversocket.getsockname()
    print("服务器地址:%s" % str(myaddr))
    # 循环等待接受客户端信息
    while True:
        # 获取一个客户端连接
        clientsocket, addr = serversocket.accept()
        print("连接地址:%s" % str(addr))
        try:
            t = ServerThreading(clientsocket)  # 为每一个请求开启一个处理线程
            t.start()
            pass
        except Exception as identifier:
            print(identifier)
            pass
        pass
    serversocket.close()
    pass


class ServerThreading(threading.Thread):
    # words = text2vec.load_lexicon()
    def __init__(self, clientsocket, recvsize=1024 * 1024, encoding="utf-8"):
        threading.Thread.__init__(self)
        self._socket = clientsocket
        self._recvsize = recvsize
        self._encoding = encoding
        pass

    def run(self):
        print("开启线程.....")
        try:
            # 接受数据
            msg = ''
            while True:
                # 读取recvsize个字节
                rec = self._socket.recv(self._recvsize)
                # 解码
                msg += rec.decode(self._encoding)
                # 文本接受是否完毕，因为python socket不能自己判断接收数据是否完毕，
                # 所以需要自定义协议标志数据接受完毕
                if msg.strip().endswith('over'):
                    wordFr = msg.split(';')[0]
                    dict = msg.split(';')[1]
                    break
            sendmsg = transDef(wordFr,dict)
            # 发送数据
            self._socket.send(("%s" % sendmsg).encode(self._encoding))
            pass
        except Exception as identifier:
            self._socket.send("500".encode(self._encoding))
            print(identifier)
            pass
        finally:
            self._socket.close()
        print("任务结束.....")

        pass

    def __del__(self):
        pass


if __name__ == "__main__":
    main()