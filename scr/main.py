# -*- coding: utf-8 -*-
import string

from itchat.content import *
import requests
import json
import itchat
import random

global robotActive
global randomNum
# global userName ='人工智障'
itchat.auto_login()
robotActive=1
# itchat.auto_login(hotReload = True)
# itchat.send(u'itchat 上线了', toUserName=searchFriendsID[u'等~等灯等灯~'])
itchat.send(u'itchat 上线了', toUserName=u'小冰')
itchat.send(u'等~等灯等灯~', toUserName=u'文件传输助手')


def dealAnswer(answer):
    if(answer=='今日水群结束'):
        randomNum=random.randint(0,4)
        if(randomNum==0):
            answer='余额不足，请及时充值'
        elif(randomNum==1):
            answer = '今日水群余额已不足，明日再来'

# 调用图灵机器人的api，采用爬虫的原理，根据聊天消息返回回复内容
def tuling(info):
    appkey = "61c5365a61b7415bb919d17ff217b0f8"
    url = "http://www.tuling123.com/openapi/api?key=%s&info=%s"%(appkey,info)
    req = requests.get(url)
    content = req.text
    data = json.loads(content)
    answer = data['text']
    return answer

# 对于群聊信息，定义获取想要针对某个群进行机器人回复的群ID函数
def group_id(name):
    df = itchat.search_chatrooms(name=name)
    return df[0]['UserName']


# 注册文本消息，绑定到text_reply处理函数
# text_reply msg_files可以处理好友之间的聊天回复
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    global robotActive
    if(msg['Content']=='start entry sequence'):
        robotActive=1
        itchat.send(u'启动！！！', msg['FromUserName'])
    itchat.send(u'我现在不在线', msg['FromUserName'])
    print(msg['FromUserName'])
    # itchat.send('%s' % tuling(msg['Text']),msg['FromUserName'])


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])


# 现在微信加了好多群，并不想对所有的群都进行设置微信机器人，只针对想要设置的群进行微信机器人，可进行如下设置
@itchat.msg_register(TEXT, isGroupChat=True)
def group_text_reply(msg):
    # 当然如果只想针对@你的人才回复，可以设置if msg['isAt']:
    global robotActive
    item = group_id(u'知乎深圳大家庭')  # 根据自己的需求设置
    print('groupID' + item)
    print('2UserName' + msg['ToUserName'])
    print('FromUserName' + msg['FromUserName'])
    # print 'StatusNotifyCode'+msg['StatusNotifyCode']
    if(robotActive):
        if msg['FromUserName'] == item:
            answer = ''
            randomNum=0

            content = msg['Content']
            content = content.strip('@人工智障 ')

            print(u'wa!!!被猪@了')
            print(msg['ToUserName'])
            if msg['isAt']:
                print(u'知乎深圳大家庭')

                print('@人工智障 ' + content)
                if(content==''):
                    randomNum=random.randint(0,6)
                    if(randomNum==0):
                        answer='爪子'
                    elif(randomNum ==1 ):
                        answer = '哇，我被猪@了'
                    elif (randomNum == 2):
                        answer = '???'
                    elif (randomNum == 3):
                        answer = '有事说撒'
                    elif (randomNum == 4):
                        answer = '在！'
                    elif (randomNum == 5):
                        answer = '谁在叫我'
                else:
                    answer=tuling(content)
                    print(answer)
                    if(content=='shutdown -s -t'):
                        robotActive=0
                        answer = 'bye~bye~'

            else:
                if(content.find('人工智障')):
                    pass
                    # answer='谁在叫我？'
            itchat.send(answer, item)


itchat.run()
