import socket
import sys
import threading
import json
import pymysql
from googletrans import Translator
import re

#调用本地词典
dict_repertoire = '/root/dict_FrToCn/24s_translation/24s/dict_24s/'
# dict_repertoire = 'D:\dict_FrToCn\\24s_translation\\24s\\dict_24s\\'
#调用数据库词典
db = pymysql.connect(host='rm-gw85nhhvwr647k45lco.mysql.germany.rds.aliyuncs.com',
                     user='spider',
                     password='heyder@20220701',
                     database='spider')
cursor = db.cursor()



def translate(data):
    data = ''.join(data)
    translator = Translator()
    trans_data = translator.translate(data, src='fr', dest='zh-cn')
    return trans_data.text

def data_pretraiter(data):

    data_fr = data
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
            return ' '.join(new_data_fr), data_garde
    except Exception:
        return ' '.join(data_fr), data_garde

def transDef(word,dict):
    dict_name = dict
    dict_path = dict_repertoire + dict_name
    #如果需要用本地词典，将下列解注释然后注释访问数据库的部分
    # with open(dict_path, encoding='utf-8') as accessoires_dict:
    #     data = json.load(accessoires_dict)
    #     emptyDict = {}
    frWord = word.lower()
    #     for each in data:
    #         emptyDict[each['wordFr']] = each['wordCn']
    cursor.execute("SELECT dest FROM spider.spider_dictionary where source='"+word+"'")
    dataDict = cursor.fetchone()
    try:
        if dataDict is not None:
            return (dataDict)
        else:
            FrWord = frWord.split(' ')[0]
            cursor.execute("SELECT dest FROM spider.spider_dictionary where source='" + FrWord+"'")
            dataDict = cursor.fetchone()
            data_apresTraitement, mot_garde = data_pretraiter(frWord.split(' ')[1:])
            fr = translate(data_apresTraitement)
            return (mot_garde+fr+dataDict[0])

    except Exception as err:
        print('transDef:',err)
        print('建议在管理端词典中添加该基础词条及翻译：'+frWord.split(' ')[0])


def transDef_ModeEtendu(word,dict):
    # dict_name = dict
    # dict_path = dict_repertoire + dict_name

    frWord = word.lower()
    cursor.execute("SELECT dest FROM spider.spider_dictionary where source='"+word+"'")
    dataDict = cursor.fetchone()
    try:
        if dataDict is not None:
            return (dataDict)
        else:
            data_apresTraitement, mot_garde = data_pretraiter(frWord)
            return (mot_garde + translate(data_apresTraitement))

    except Exception as err:
        print(err)


def main():
    # 创建服务器套接字
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取本地主机名称
    host = socket.gethostname()
    # 设置一个端口
    port = 10086
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
            print('main:',identifier)
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
                if msg.strip().endswith(',over'):
                    wordFr = msg[:-5]
                    print(wordFr)
                    dict = 'accessoires_dict'
                    break
            sendmsg = transDef(wordFr,dict)
            if sendmsg is None:
                sendmsg = translate(wordFr)
                print('添加整句词条及其翻译：'+wordFr)
            # 发送数据
            self._socket.send(("%s" % sendmsg).encode(self._encoding))
            pass
        except Exception as identifier:
            self._socket.send("500".encode(self._encoding))
            print('run:',identifier)
            pass
        finally:
            self._socket.close()
        print("任务结束.....")

        pass

    def __del__(self):
        pass


if __name__ == "__main__":
    main()