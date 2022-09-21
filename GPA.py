import requests
from bs4 import BeautifulSoup

url = 'http://ams.bhsfic.com/system/login/doLogin'
website = requests.get('http://ams.bhsfic.com/system/login').text
session = requests.Session()

account = input('请输入你的学号：')
password = input('请输入你的密码：')

headers = {
    'Host': 'ams.bhsfic.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Referer': 'http://ams.bhsfic.com/system/login',
    'Origin': 'http://ams.bhsfic.com',
}

ams = session.post(url=url, data={'email': account, 'userPwd': password}, headers=headers)
ams.encoding = 'utf-8'

if ams.text != website and ams.status_code == 200:
    bs = BeautifulSoup(ams.text, 'lxml')
    GPA = bs.find('div', class_='top-index').find('b').text
    behavior_GPA = bs.find('div', class_="top-index").find(id='behavior').find('b').text
    name = bs.find(class_='text-muted text-xs block').text
    print(name.strip().replace('\n', ''), GPA, behavior_GPA)
    print()

    headers = {
        'Referer': 'http://ams.bhsfic.com/student/calendar/calendarPage',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }

    Academic_Report = session.get('http://ams.bhsfic.com/student/behavior/studentGpa', headers=headers).text
    score = BeautifulSoup(Academic_Report, 'lxml').findAll('td')
    for i in range(1, len(score)):
        if i-int(i/10)*10 == 1:
            print(score[i].text.replace('\n', '').replace('\t', '').replace(' ', '', 1))
        if 4 == i-int(i / 10)*10:
            print("期中考试:", score[i].text.replace('\n', '').replace('\t', '').replace(' ', '', 1),
                  '期末考试:' ,score[i+1].text.replace('\n', '').replace('\t', '').replace(' ', '', 1),
                  '总分:', score[i+2].text.replace('\n', '').replace('\t', '').replace(' ', '', 1),
                  '总评:', score[i+3].text.replace('\n', '').replace('\t', '').replace(' ', '', 1))

elif ams.status_code != 200:
    print("页面错误")