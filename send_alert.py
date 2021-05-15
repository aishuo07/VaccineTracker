import json
import time
import datetime
import requests
import smtplib
import pymongo

client = pymongo.MongoClient("mongodb+srv://Aish:Aish1234@cluster0.lrwnk.mongodb.net/Cowin?retryWrites=true&w=majority")
db = client["db"]
col = db["bucketList"]

headers = {
        'Host': 'cdn-api.co-vin.in',
        'Connection': 'close',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'Accept': 'application/json, text/plain, /',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'Origin': 'https://www.cowin.gov.in',
        "Sec-Fetch-Site": 'cross-site',
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        "Referer": 'https://www.cowin.gov.in/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7'
}

my_email =  "getvaccinated3@gmail.com"
password = "Aish@1234"

def getdate():
    return datetime.datetime.today().strftime('%d-%m-%Y')
    

def getrequest(pincode):
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=" +pincode+ "&date=" + getdate()
    return requests.get(URL, headers = headers).json()


def get_List(x, dic):
    for i in x:
        r = getrequest(i['pincode'])
        print("checked for: " + i['email'])
        message = '\n Vaccine available at :'
        flag, count = False, 1
        if 'error' in r:
            continue
        for j in r['centers']:
            if j['sessions'][0]["available_capacity"]>0:
                flag = True
                message += '\n{}.) Center Name -  {} \n Address - {} \n Vaccine available - {} \n Date - {}\n'.format(count, j['name'], j['address']  + ', ' + j["district_name"] + ', ' + j["state_name"], j["sessions"][0]["available_capacity"], j["sessions"][0]["date"])
                count+=1
        if flag and i['email'] not in dic:
            send_mail(i['email'], message)

def send_mail(email, message):
    SUBJECT = "Vaccine available"
    mess = 'Subject: {}\n\n{}'.format(SUBJECT, message)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(my_email, password)
    s.sendmail(my_email,email, mess)
    s.quit()
    print("mail sent to "+email)
    dic[email] = None

c, dic = 0, {}
while True:
    x = col.find()
    get_List(x, dic)
    c+=1
    time.sleep(10)
    if c == 600:
      c = 0
      dic = {}