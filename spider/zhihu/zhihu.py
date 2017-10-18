"""
    模拟登陆知乎
"""
import time
from http import cookiejar

import requests
from bs4 import BeautifulSoup

headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.102 Safari/537.36 Vivaldi/1.93.955.38"
}

# 使用登陆cookie信息，用于持久化连接
session = requests.Session()
session.cookies = cookiejar.LWPCookieJar(filename='cookies.txt')

try:
    # 后续调用session.cookies.save()保存cookies到cookies.txt文件中
    session.cookies.load(ignore_discard=True)
except:
    print("还没有cookie信息")

def get_xsrf():
    '''
        获取xsrf的值
    '''
    response = session.get("https://www.zhihu.com", headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    xsrf = soup.find('input', attrs={"name": "_xsrf"}).get("value")
    return xsrf

def get_captcha():
    """
    把验证码图片保存到当前目录，手动识别验证码
    :return:
    """
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login" + "&lang=en"
    # print(captcha_url)
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
    captcha = input("验证码：")
    return captcha


def login(phone_num, password):
    '''
        模拟登陆
    '''
    login_url = "https://www.zhihu.com/login/phone_num"
    data = {
        "phone_num": phone_num,
        "password": password,
        "captcha": get_captcha(),
        "_xsrf": get_xsrf() 
    }

    # 把cookie保存到文件中，执行一次就够了
    # session.cookies.save()

    response = session.post(login_url, data=data, headers=headers)

    login_code = response.json()
    # print(login_code['msg'])
    # print(session.cookies)

    r = session.get("https://www.zhihu.com/settings/profile", headers=headers)
    print(r.status_code)
    # print(r.text)
    with open('xx.html', 'wb') as f:
        f.write(r.content)


if __name__ == "__main__":
    phone_num = "xxxxxx"
    password = "xxxxxxx"
    login(phone_num, password)
