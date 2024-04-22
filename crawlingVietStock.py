import requests
from datetime import * 
import re 
import csv 
# redefine Headers
headers = {
    "Host": "api.vietstock.vn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Referer": "https://finance.vietstock.vn/",
    "Connection": "close"
}
# api 
url = "https://api.vietstock.vn/finance/toptrading?type=7&catID=1"

proxies = { 'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

# send request and use burpsute as proxy to debug
r = requests.get(url, headers=headers, proxies=proxies, verify=False)

data = r.json()
stockCode =[]
# use only StockCode 
for i in data:
    stockCode.append(i['StockCode'])

# define cookie to verify request 
cookie = {"__RequestVerificationToken":"oOc41mm2k_ow0mCIx1pQICHMyb0WqfsIrV9Cy4Lo967Gxw1gYQ2cAYfCH2IDLrI91ZpGXfBXQCfTxyCIrfYPlGHFUiU-VeR-AvcYW30OBMo1"}
# redefine headers
headers ={"Host": "finance.vietstock.vn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://finance.vietstock.vn/SSI/thong-ke-giao-dich.htm",
        "Connection": "close"
}
# api which to send request
url = "https://finance.vietstock.vn/data/gettradingresult"
# define date 
today = date.today()
before = today - timedelta(days=30)
# format Date 
def dateFomat(d):
    day = re.sub(r'\D','', d)
    day = int(day)/1000
    day = datetime.fromtimestamp(day)
    return str(day)

csvData = {"Date":[]}

for i in stockCode:
    csvData[i] = []
    print("Stock Code: ", i)
    data = "Code={code}&OrderBy=&OrderDirection=desc&PageIndex=1&PageSize=30&FromDate={past}&ToDate={now}&ExportType=default&Cols=TKLGD%2CTGTGD%2CVHTT%2CTGG%2CDC%2CTGPTG%2CKLGDKL%2CGTGDKL&ExchangeID=1&__RequestVerificationToken=AmplTSPhLRNUD4lyFsJbQzVgMe3uR-UCu_aZFVmh8j_S_G3xbpZ8s1D2VyWfowbZEWZVYH10ySAxjRdoO1tdpcXZ_D-YPDhVKXLgEJLT_Ao1".format(code = i, past = before, now = today)
    r = requests.post(url, headers=headers, cookies= cookie, data=data, proxies=proxies,verify=False)
    # parse json date to normal date 
    codeInfor = r.json()
    
    for j in codeInfor["Data"]:
        # print(dateFomat(j["TradingDate"]), j["ClosePrice"], sep=' : ') 
        if len(csvData["Date"]) < 30:
            # advoid identical data
            csvData['Date'].append(dateFomat(j["TradingDate"]))
        csvData[i].append(j["ClosePrice"])

with open("csvData.csv", "w") as outfile:
    writer = csv.writer(outfile)
    # use dictionary key for row
    writer.writerow(csvData.keys())
    writer.writerows(zip(*csvData.values()))
