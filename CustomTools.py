import datetime

class FunctionGroup:

    def getRawData(method,date,lat,sat):
        return 'method='+method+'&secDateStr=&secId=&divId=&licenseTypeCode=3&expectExamDateStr='+date+'&_onlyWeekend=on&dmvNoLv1='+lat+'&dmvNo='+sat
    
    def getStateHeader():
        return {
        'Connection': 'keep-alive',
        'Content-Length': '119',
        'Origin': 'https://www.mvdis.gov.tw',
        'Host': 'www.mvdis.gov.tw',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Referer': 'https://www.mvdis.gov.tw/m3-emv-trn/exm/locations',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control':'max-age=0',
        'Sec-Fetch-Mode':'navigate',
        'Sec-Fetch-Site':'same-origin',
        'Sec-Fetch-User':'?1',
        'Upgrade-Insecure-Requests':'1',
        'Cookie': '_ga=GA1.3.1624244803.1566046944; _gid=GA1.3.1995601693.1566046944; JSESSIONID2=6CC2305A36B7602867C1A8C410AECF17.tsp41; JSESSIONID1=636682CF99D8FB5D7ACF031F06527FBE.tsp12'
        }
    
    def getStationHeader():
        return {
        'Connection': 'keep-alive',
        'Content-Length': '125',
        'Origin': 'https://www.mvdis.gov.tw',
        'Host': 'www.mvdis.gov.tw',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Referer': 'https://www.mvdis.gov.tw/m3-emv-trn/exm/locations',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control':'max-age=0',
        'Sec-Fetch-Mode':'navigate',
        'Sec-Fetch-Site':'same-origin',
        'Sec-Fetch-User':'?1',
        'Upgrade-Insecure-Requests':'1',
        'Cookie': '_ga=GA1.3.1624244803.1566046944; _gid=GA1.3.1995601693.1566046944; JSESSIONID2=6CC2305A36B7602867C1A8C410AECF17.tsp41; JSESSIONID1=636682CF99D8FB5D7ACF031F06527FBE.tsp12'
        }
    
    def dmvCityLocation():
        return [['臺北市區','20'],['臺北區','40'],['新竹區','50'],['臺中區','60'],['嘉義區','70'],['高雄市區','30'],['高雄區','80']]
    
    def checkCityExist(num):
        tmp = 'null'
        for i in range(len(FunctionGroup.dmvCityLocation())):
            if(num == FunctionGroup.dmvCityLocation()[i][1]):
                tmp = FunctionGroup.dmvCityLocation()[i][0]
                break
        return tmp
    
    def checkStaExist(mylist,num):
        tmp = 'null'
        for i in mylist:
            tmpW = i.split(",")
            if(num == tmpW[0]):
                tmp = tmpW[1]
                break
        return tmp
    
    def getDate():
        x = datetime.datetime.now() #現在時間
        dateW = str(x.year-1911)
        if(x.month <10):
            dateW += "0"+str(x.month)
        else:
            dateW += str(x.month)

        if(x.day <10):
            dateW += "0"+str(x.day)
        else:
            dateW += str(x.day)

        return dateW