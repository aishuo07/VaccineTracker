import json
import time
from datetime import date
import requests
import smtplib
import pymongo

client = pymongo.MongoClient("mongodb+srv://Aish:Aish1234@cluster0.lrwnk.mongodb.net/Cowin?retryWrites=true&w=majority")
db = client["db"]
col = db["bucketList"]

http_proxy  = "http://ec2-65-1-80-176.ap-south-1.compute.amazonaws.com:8888"
https_proxy = "http://ec2-65-1-80-176.ap-south-1.compute.amazonaws.com:8888"
ftp_proxy   = "ftp://10.10.1.10:3128"

proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy, 
            }
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

def get_List(x):
    t_date = str(date.today()).split('-')[::-1]
    d = ''
    for i in t_date[:-1]:
          d+=i + '-'
    d+=t_date[-1]
    for i in x:
        r = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=" + i['pincode'] + "&date=" + d, headers = headers, proxies=proxyDict)
        c = r.json()
        print("checked for: " + i['email'])
        message = '\n Vaccine available at :'
        flag = False
        count = 1
        for j in c['centers']:
            print(j['sessions'][0]["available_capacity"])
            if j['sessions'][0]["available_capacity"]>0:
                flag = True
                message += '\n{}.) Center Name -  {} \n Address - {} \n Vaccine available - {} \n Date - {}\n'.format(count, j['name'], j['address']  + ', ' + j["district_name"] + ', ' + j["state_name"], j["sessions"][0]["available_capacity"], j["sessions"][0]["date"])
                count+=1
        if flag:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("getvaccinated3@gmail.com", "Aish@1234")
            s.sendmail("getvaccinated3@gmail.com",i['email'], message)
            s.quit()

while True:
    x = col.find()
    get_List(x)
    time.sleep(60)