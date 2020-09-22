import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

login_url = 'http://pdc.police.go.th/index.php'
url_out = "http://pdc.police.go.th/arrest_search?KT_logout_now=1"
get_url = 'http://pdc.police.go.th/smart_c.php'
get_url3 = 'http://pdc.police.go.th/result_aa.php'
wan_url=''
now = datetime.now()

url = 'https://notify-api.line.me/api/notify'
token = 'cW3MsD9e9Qod9OyrPzTzRCF8MroAl91PnMlRSysxBER'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}


payload1 = {
    'hiddenField': '2020-03-15 12:58:59',
    'username': 'pdc',
    'password': '1632',
    'kt_login1': '',
    'token': ''
    
}

payload2 = {
    'smart': '0' 
}

payload3 = {
    'fname' : '0'
}

login_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate'
}

def listToString(s):  
    
    # initialize an empty string 
    str1 = "" 
    
    # return string   
    return (str1.join(s)) 

def tableDataText(table):
        rows = []
        trs = table.find_all('tr')
        headerow = [td.get_text(strip=True) for td in trs[0].find_all('th')]
        if headerow: # if there is a header row include first
            rows.append(headerow)
            trs = trs[1:]
            for tr in trs: # for every table row
                rows.append([td.get_text(strip=True) for td in tr.find_all('td')]) # data row
                return rows
def pdcfind(ss):
        result = 0
        i = 0
        with requests.Session() as session:
            msx = []
            payload2['smart'] = ss
            dt_string = now.strftime("%y-%m-%d %H:%M:%S")
            payload1['hiddenField'] = dt_string
            post = session.post(login_url, data=payload1)
            print(post.text)
            r = session.post(get_url, data=payload2)
            r.encoding = 'utf-8'
            html = r.text
            soup = BeautifulSoup(html, "html.parser")
            page = soup.find('p').getText()
            htmltable = soup.find('table', { 'id' : 'mydata' })
            if page != "จำนวน 0 หมาย" :
                for a in htmltable.find_all('a', href=True):
                    i+=1
                    wan_url = "http://pdc.police.go.th/"+a['href']
                    x = session.post(wan_url)
                    x.encoding = 'utf-8'
                    htmlwan = x.text
                    soupwan = BeautifulSoup(htmlwan, "html.parser")
                    array = []
                    for b in soupwan.find_all('td'):
                        array.append(b.text.replace("\n", " ").replace("  ", " ").replace("\xa0", ""))
                    jj = ("บัตรประชาชน :"+array[1]+"  สถานะ :"+array[19]+"  หมายจับที่ :"+array[9]+"  คดีอาญาที่ :"+array[13]+"  ข้อหา :"+array[11]+"  สภ.เจ้าของหมาย :"+array[23])
                    msx.append(jj)
                list_table = tableDataText(htmltable)
                msg_line1 = "ชื่อ : "+list_table[1][2]+"  พบหมายจับ "+str(i)+" หมาย"+"\n"
                line_msg = []
                for k in range(i):
                    line_msg.append("("+str(k+1)+")"+msx[k]+"\n")
                msg_line2 = listToString(line_msg)
                line_send = msg_line1+msg_line2
                logout = session.post(url_out)
                return line_send
            else:
                line_send = "ไม่พบหมายจับ"
                logout = session.post(url_out)
                return line_send        
        #r = requests.post(url, headers=headers , data = {'message':line_send})

def pdcfindname(sn):
        result = 0
        i = 0
        with requests.Session() as session:
            msx = []
            payload3['fname'] = sn
            dt_string = now.strftime("%y-%m-%d %H:%M:%S")
            payload1['hiddenField'] = dt_string
            post = session.post(login_url, data=payload1, headers=login_headers)
            #post = session.post(login_url, data=payload1)
            r = session.post(get_url3, data=payload3)
            r.encoding = 'utf-8'
            html = r.text
            soup = BeautifulSoup(html, "html.parser")
            page = soup.find('p').getText()
            htmltable = soup.find('table', { 'id' : 'mydata' })
            if page != "พบ 0 หมาย" :
                for a in htmltable.find_all('a', href=True):
                    i+=1
                    wan_url = "http://pdc.police.go.th/"+a['href']
                    x = session.post(wan_url)
                    x.encoding = 'utf-8'
                    htmlwan = x.text
                    soupwan = BeautifulSoup(htmlwan, "html.parser")
                    array = []
                    for b in soupwan.find_all('td'):
                        array.append(b.text.replace("\n", " ").replace("  ", " ").replace("\xa0", ""))
                    jj = ("บัตรประชาชน :"+array[1]+"  สถานะ :"+array[19]+"  หมายจับที่ :"+array[9]+"  คดีอาญาที่ :"+array[13]+"  ข้อหา :"+array[11]+"  สภ.เจ้าของหมาย :"+array[23])
                    msx.append(jj)
                list_table = tableDataText(htmltable)
                msg_line1 = "ชื่อ : "+list_table[1][3]+"  พบหมายจับ "+str(i)+" หมาย"+"\n"
                line_msg = []
                for k in range(i):
                    line_msg.append("("+str(k+1)+")"+msx[k]+"\n")
                msg_line2 = listToString(line_msg)
                line_send = msg_line1+msg_line2
                logout = session.post(url_out)
                return line_send
            else:
                line_send = "ไม่พบหมายจับ"
                logout = session.post(url_out)
                return line_send        
        #r = requests.post(url, headers=headers , data = {'message':line_send})



def line_send(message):
    r = requests.post(url, headers=headers, data={'message': message})
    print(r.text)