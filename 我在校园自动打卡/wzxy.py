import datetime
import json
import logging
import smtplib  # smtp服务器
from email.mime.text import MIMEText  # 邮件文本

import random
import requests
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# 日检日报提交后字典的参数，返回中文
def get_status1(self):
    if self['code'] == 0:
        # return "日检日报成功"
        return "自动打卡(日检日报)成功"
    elif self['code'] == 1:
        return "日检日报打卡时间结束"
    elif self['code'] == -10:
        return "jwsession已失效,请及时更换jwsession值"
    else:
        return "发生未知错误,请及时检查!"


# 健康打卡提交后字典的参数，返回中文
def get_status2(self):
    if self['code'] == 0:
        return "自动打卡(健康打卡)成功"
    elif self['code'] == 1:
        return "健康打卡时间结束"
    elif self['code'] == -10:
        return "jwsession已失效,请及时更换jwsession值"
    else:
        return "发生未知错误,请及时检查!"


def sendemail(receiver, content):
    subject = "我不在校园打卡"  # 邮件标题
    host_server = 'smtp.qq.com'
    sender = "wxshuai1025@qq.com"  # 发送方
    recver = receiver  # 接收方的邮箱号
    password = "dpzqasvehwwhdjja"  # 刚刚设置是复制的授权密码; 注意是授权密码, 不是邮箱密码
    message = MIMEText(content, "plain", "utf-8")  # content:发送内容; "plain":文本格式; utf-8:编码格式
    message['Subject'] = subject  # 邮件标题
    message['To'] = recver  # 收件人
    message['From'] = sender  # 发件人
    smtp = smtplib.SMTP_SSL(host_server)  # 实例化smtp服务器,如果是126网易邮箱用这个
    # smtp = smtplib.SMTP_SSL("smtp.163.com", 994) #实例化smtp服务器,如果是163网易邮箱就用这个
    smtp.login(sender, password)  # 发件人登录
    smtp.sendmail(sender, [recver], message.as_string())  # as_string 对 message 的消息进行了封装
    smtp.quit()


class Do:
    def __init__(self):
        # 几个接口
        self.api1 = "https://student.wozaixiaoyuan.com/heat/save.json"  # 日检日报 提交地址
        self.api2 = "https://student.wozaixiaoyuan.com/health/save.json"  # 健康打卡 提交地址
        self.api3 = "https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username"  # 账号密码登录地址

        self.email_sender = "2444059324@qq.com"  # 邮件发送者
        self.jwsession = ""  # JWsession
        self.tokenName = ""  # 可写微信昵称
        self.username = ""  # 用户账号
        self.password = ""  # 密码
        self.email = ""  # 接收结果的邮箱
        self.user_dict = {  # 用户列表字典
            "0": {
                "username": "18991638241",
                "password": "shuai2001102",
                "email": "2444059324@qq.com",
                "nickname": "wxs"
            },
        }
        self.headers = {
            "Host": "student.wozaixiaoyuan.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI "
                          "MiniProgramEnv/Windows WindowsWechat",
            "Referer": "https://servicewechat.com/wxce6d08f781975d91/186/page-frame.html",
            # "Content-Length": "331",
        }  # 以上都可以在抓包中获取参数信息

        # 日检日报数据
        self.data1 = {
            "answers": '["0"]',
            "seq": self.get_seq(),
            "temperature": self.get_random_temprature(),  # 通过随机函数进行填写体温数据
            "latitude": "34.15775",  # 维度
            "longitude": "108.90688",  # 经度
            "country": "中国",
            "city": "西安市",
            "district": "长安区",
            "province": "陕西省",
            "township": "韦曲街道",
            "street": "西长安街",
        }  # 位置信位息也是通过抓包获取之前是记录

        # 健康打卡数据
        self.data2 = {
            "answers": f'["0","1","{self.get_random_temprature()}℃"]',  # 保险起见, 默认只选第一个, 根据自己的界面选项选
            # "answers": '["0","3","1","无","无","0"]', #打卡界面的选项参数
            # 把answers属性的值改为'["0","1","1",,"0","xxxxx","1"]'（xxxxx为填入的信息）
            # 其中0代表问题的第一个选项，1代表问题的第二个选项，以此类推就行.(根据需要填写).
            # 但是填选问题有风险,就是如果小程序里的选项发生变动,就会可能填错信息,
            # 那就只能时不时去看一下有没有信息变动
            "latitude": "34.15775",  # 维度
            "longitude": "108.90688",  # 经度
            "country": "中国",
            "city": "西安市",
            "district": "长安区",
            "province": "陕西省",
            "township": "韦曲街道",
            "street": "西长安街",
            "areacode": "610116",
            "towncode": "610116001",
            "citycode": "156610100",
            "timestampHeader": str(round(time.time() * 1000)),  # 时间戳标头
            # "signatureHeader": "4a1e8f32508cefce4f7779feadc8ea76e4b72c1edc02a08f005b1bd60693d905",#签名头
        }  # 位置信息也是通过抓包获取之前是记录

    # 自动登录获取jwsession
    def get_jwession(self):
        data = "{}"
        session = requests.session()
        url = self.api3 + "?username=" + self.username + "&password=" + self.password
        respt = session.post(url, data=data, headers=self.headers)
        res = json.loads(respt.text)
        if res["code"] == 0:
            print("登录成功")
            self.jwsession = respt.headers['JWSESSION']
            print("成功获取到jsession：" + self.jwsession)
            return True
            # return jwsession
        else:
            print(res['message'])
            return False

    # 获取随机体温
    def get_random_temprature(self):
        random.seed(time.ctime())
        t1 = random.randint(3, 7)
        t2 = random.randint(3, 7)
        while t1 == t2:
            t1 = random.randint(3, 7)
            t2 = random.randint(3, 7)
        return f"36.{random.choice([t1, t2])}"

    # seq的1,2,3代表着早，中，晚
    def get_seq(self):
        current_hour = datetime.datetime.now()
        # current_hour = current_hour.hour + 8
        current_hour = current_hour.hour
        if 0 <= current_hour <= 8:
            return "1"
        elif 11 <= current_hour < 14:
            return "2"
        elif 17 <= current_hour < 20:
            return "3"
        else:
            return "1"

    def run(self):
        for key, value in self.user_dict.items():
            self.username = value['username']
            self.password = value['password']
            self.email = value['email']
            self.tokenName = value['nickname']
            if self.get_jwession():  # 获取jwession
                self.headers["JWSESSION"] = self.jwsession
                # print(datetime.datetime.now())
                # res1 = requests.post(self.api1, headers=self.headers, data=self.data1, ).json()  # 日检日报
                # time.sleep(1)
                # print(res1)

                if self.get_seq():  # == "1":
                    # print(self.data2)
                    res2 = requests.post(self.api2, headers=self.headers, data=self.data2, ).json()  # 健康打卡提交

                    time.sleep(1)
                    # print(res2)

                    # 调用发邮件函数
                    sendemail(self.email_sender,
                              self.tokenName + ",现在进行云端自动打卡" + "\n" + get_status2(
                                  res2) + "\n" + "哈哈哈\n" + "打卡时间为:" + str(datetime.datetime.now()))
                """
                else:
                    # 调用发邮件函数
                    sendemail("2444059324@qq.com",
                              self.tokenName[num] + ",现在进行云端自动打卡" + "\n" + get_status1(res1) + "\n哈哈\n" + "打卡时间为:" + str(
                                  datetime.datetime.now()))
                """
            else:  # jwession获取异常(不排除用户名或密码错误)
                # 调用发邮件函数
                sendemail(self.email_sender,
                          self.tokenName + ",jwsession获取失败，请通知管理员检查程序！\n" + "打卡时间为:" + str(datetime.datetime.now()))
        current_hours = datetime.datetime.now()
        # current_hours = current_hours.hour
        print(current_hours)
        return True


if __name__ == "__main__":
    Do().run()


def main_handler(event, context):
    logger.info('got event{}'.format(event))
    return Do().run()
