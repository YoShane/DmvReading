import requests
import pandas as pd
from bs4 import BeautifulSoup
from CustomTools import FunctionGroup
import time
import threading
import datetime
import smtplib
from email.mime.text import MIMEText
import os

dmvLocation = FunctionGroup.dmvCityLocation()
currentLat = '0' #區域代號
currentSat = '0' #監理站代號
endDate = '2019-08-29'
global d1
global refreshCount
global sendCount
global hasReg
d1 = datetime.datetime(2019,8,19)
refreshCount = 0
sendCount = 0
hasReg = False
requests.adapters.DEFAULT_RETRIES = 5

print("歡迎進入系統，請選擇監理站區域")
for i in range(len(dmvLocation)):
    print("　"+str(i+1)+".",end="")
    for j in dmvLocation[i]:
        print(j,end="")
        if(len(j)<4):
            print("　",end="") #補間距
    print()

while(FunctionGroup.checkCityExist(currentLat) == 'null'):
    currentLat = input("輸入後方代號: ") 

print("Loading...") #讀取監理站名稱
res = requests.post("https://www.mvdis.gov.tw/m3-emv-trn/exm/locations",
                    headers=FunctionGroup.getStationHeader(), data=FunctionGroup.getRawData('dmvOnChange',FunctionGroup.getDate(),currentLat,currentSat))
soup = BeautifulSoup(res.text, 'html.parser') #進一步內容處理-格式化                  
tmpW = str(soup.find_all('select',{"id": "dmvNo"})) #找監理站下拉選單
tmpW = tmpW.split("</option>") #先分開每個監理站
tmpList = []
dmvList = []
for i in tmpW:
    if ("站" in i or "所" in i):
        tmpList.append(i) #只放監理站或監理所
for i in tmpList:
    newName = i.replace('\n<option value="','') #取代多餘html文字
    newName = newName.replace('">',',')
    dmvList.append(newName)
    
os.system("cls") #清除畫面
        
print("選擇考機車駕照地點 in"+FunctionGroup.checkCityExist(currentLat))
for i in dmvList:
    tmpW = i.split(",")
    print("　"+tmpW[0]+" ->"+tmpW[1])
while(FunctionGroup.checkStaExist(dmvList,currentSat) == 'null'):
    currentSat = input("輸入監理站代號: ")

def runReading():
    global d1
    global refreshCount
    global sendCount
    global hasReg
    refreshCount = refreshCount + 1
    print("Loading...") #讀取報名狀態
    res = requests.session()
    res.keep_alive = False #關閉多餘連線
    res = requests.post("https://www.mvdis.gov.tw/m3-emv-trn/exm/locations",
                        headers=FunctionGroup.getStateHeader(), data=FunctionGroup.getRawData('query',FunctionGroup.getDate(),currentLat,currentSat))
    #print(res.request.headers) # 看requests送出的header
    #print(res.text)
    os.system("cls") #清除畫面

    print(FunctionGroup.checkCityExist(currentLat) +"監理所")
    print(FunctionGroup.checkStaExist(dmvList,currentSat))

    df = pd.read_html(res.text)[8]
    date = pd.Series(df['考試日期 (星期) Date of Test'])
    group = pd.Series(df['場次組別說明 Desc.'])
    people = pd.Series(df['可報名人數 Number'])
    total_data = pd.DataFrame({'date':date, 'group':group, 'people':people})

    total_data['date'] = total_data['date'].str.replace("108","2019") #取代字串以便後續格式化
    total_data['date'] = total_data['date'].str.replace("109","2020")
    total_data['date'] = total_data['date'].str.replace("年","-")
    total_data['date'] = total_data['date'].str.replace("月","-")
    total_data['date'] = total_data['date'].str.replace("日 ","")
    total_data['date'] = total_data['date'].str.replace("星期一","")
    total_data['date'] = total_data['date'].str.replace("星期二","")
    total_data['date'] = total_data['date'].str.replace("星期三","")
    total_data['date'] = total_data['date'].str.replace("星期四","")
    total_data['date'] = total_data['date'].str.replace("星期五","")
    total_data['date'] = total_data['date'].str.replace("星期六","")
    total_data['date'] = total_data['date'].str.replace("星期日","")
    total_data['date'] = total_data['date'].str.replace('(',"")
    total_data['date'] = total_data['date'].str.replace(')',"")

    total_data['date'] = pd.to_datetime(total_data['date']) #將資料型別轉換為日期型別
    total_data['people'] = total_data['people'].astype(str) #將人數轉字串
    mask = total_data['date'] <= endDate #篩選時間存入遮罩
    total_data = total_data.loc[mask] #扣除false的內容

    first_test = total_data[(total_data.group.str.contains('本場次為重考生')==False)] #排除重考生
    first_test = first_test.reset_index(drop = True) #重設id
    empty_people = first_test[first_test.people != '額滿'] #排除額滿
    output_date = empty_people['date']

    if(output_date.size >0):
        
        print(first_test)
        print()
        print("以上為目前狀態"+"(更新次數:"+str(refreshCount)+")")
        print("V 以下為可報名日期")
        print(output_date)
        print("Total:", output_date.size)

        if not hasReg:
            #目前預約報名 身分證=L225072148 生日=0900808
            hasReg = True
            date = empty_people.iloc[0,0].strftime("%Y-%m-%d") #取得第一個的日期
            sec = '1'
            if("下午" in empty_people.iloc[0,1]):
                sec = '2'
            print("嘗試報名中")
            sat = str(currentSat)
            div = '3'
            requests.post("https://www.mvdis.gov.tw/m3-emv-trn/exm/signUp",
                        headers=FunctionGroup.getAddHeader(), data=FunctionGroup.getAddData(date,sat,div,sec))
            print(FunctionGroup.getAddData(date,sat,div,sec))
            
        d2 = datetime.datetime.now()
        interval = d2 - d1
        sec = interval.days*24*3600 + interval.seconds
        if(sec >= 600): #超過時間可以再記一次信
            print('Email start!')
            sendW = '以下為可報名日期，請及時前往預約\nhttps://www.mvdis.gov.tw/m3-emv-trn/exm/locations\n'+str(output_date)
            gmail_user = '寄信@email'
            gmail_password = '寄信密碼' # your gmail password
            msg = MIMEText(sendW)
            msg['Subject'] = '機車考照預約有名額囉'
            msg['From'] = gmail_user
            msg['To'] = '收信人@email'
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.send_message(msg)
            server.quit()
            print('Email sent!')
            d1 = datetime.datetime.now()
            sendCount = sendCount + 1

    else:
        print(first_test)
        print()
        print("以上為目前狀態"+"(更新次數:"+str(refreshCount)+")")
        print("X 尚未釋出報名名額")

    if(sendCount != 0):
        print("傳送次數:"+str(sendCount))
    threading.Timer(30, runReading).start()

runReading()
