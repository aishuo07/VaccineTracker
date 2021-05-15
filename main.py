import requests
import datetime
from flask import Flask, render_template, request, jsonify
import json
import pymongo

app = Flask(__name__, static_url_path='/static')
mongo = pymongo.MongoClient("mongodb+srv://Aish:Aish1234@cluster0.lrwnk.mongodb.net/Cowin?retryWrites=true&w=majority")
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/availabilty', methods=['GET', 'POST'])
def availabilty():
    pincode = request.form.get('Pincode')
    d = ''
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
    d = datetime.datetime.today().strftime('%d-%m-%Y')
    print(d)
    r = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=" + str(pincode) + "&date=" + d, headers = headers)
    print(r)
    c = r.json()
    return render_template('table.html', loc_data = c)


@app.route('/addwhatsapp', methods=['GET', 'POST'])
def addnumber():
    bucketList = mongo.db.bucketList
    res = request.json
    jso = {'pincode':res['pincode'], "number": res['number'], 'email':''}
    if bucketList.find(jso).count() == 0:
        bucketList.insert()
    return render_template('index.html')
    

@app.route('/addemail', methods=["GET", "POST"])
def addemail():
    if request.method == "POST":
        bucketList = mongo.db.bucketList
        jso = {'pincode':request.form['Pincode'], "number": '', 'email':request.form['email']}
        if bucketList.find(jso).count() == 0:
            bucketList.insert(jso)
            print("Inserted")
            return render_template('index.html')
        else:
            return render_template('newsletter.html')
    else:
        return render_template('newsletter.html')


    
if __name__ == '__main__':
    app.run()
