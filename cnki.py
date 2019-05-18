import requests
from lxml import etree
import re
import time
import random
import pymysql
import datetime

data = {
    'sorttype':'TIME',
    'action':' ',
    'NaviCode':'*',
    'ua':'1.21',
    'isinEn':'1',
    'PageName':'ASP.brief_result_aspx',
    'DbPrefix':'SCDB',
    'DbCatalog':'中国学术文献网络出版总库',
    'ConfigFile':'SCDB.xml',
    'db_opt':'CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD',
    'publishdate_from':'2019-01-01',
    'publishdate_to':'2019-05-16',
    'au_1_sel':'AU',
    'au_1_sel2':'AF',
    'au_1_value2':'南京大学',
    'au_1_special1':'=',
    'au_1_special2':'%',
    'his':'0',
    '__':'Fri May 17 2019 14:43:08 GMT+0800 (中国标准时间)'

}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24'
}

users = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
]

db = pymysql.connect("localhost", "root", "123456", "test0")
cursor = db.cursor()

def parse_detail(url,sj):
    # urlc = 'http://kns.cnki.net/KCMS/detail/detail.aspx?dbcode=CJFQ&dbname=CJFDTEMP&filename=XDFC20190404003'

    res = s.get(url, headers=headers)
    # print(res.text)
    e = etree.HTML(res.text)
    text = e.xpath('//*[@id="mainArea"]//h2/text()')[0]
    isbn = e.xpath('//*[@class="sourinfo"]/p[4]/text()')[0].strip()
    authors = e.xpath('//*[@class="author"]/span')
    organs = e.xpath('//*[@class="orgn"]/span')
    # sj = e.xpath('//*[@class="head-tag"]/div/b/text()')[0]
    # doi = e.xpath('//*[@id="catalog_ZCDOI"]/../text()')[0]
    authorlist = []
    organlist = []
    for author in authors:
        authorname = author.xpath('a/text()')[0]
        # print(authorname)
        authorlist.append(authorname)

    for organ in organs:
        organname = organ.xpath('a/text()')[0]
        # print(organname)
        organlist.append(organname)
    authors = ','.join(authorlist)
    organs = ','.join(organlist)
    print(text, isbn,authors,organs)
    sql = """ INSERT INTO CNKI(title,isbn,author,organ,time) VALUES ('%s','%s','%s','%s','%s')"""%(text,isbn,authors,organs,sj)
    try:
        cursor.execute(sql)
        db.commit()
        print('successful')
    except:
        db.rollback()
def parse_detaile(url,sj):
    res = s.get(url, headers=headers)
    e = etree.HTML(res.text)
    text = e.xpath('//*[@id="mainArea"]//h2/text()')[0]
    print(text)
    # isbn = e.xpath('//*[@class="sourinfo"]/p[4]/text()')[0].strip()
    isbn = e.xpath('//*[@target="_blank"]/text()')[0].strip()
    print(isbn)
    authors = e.xpath('//*[@class="authorE"]/span')
    organs = e.xpath('//*[@class="orgnE"]/span')
    authorlist = []
    organlist = []
    for author in authors:
        authorname = author.xpath('a/text()')[0]
        # print(authorname)
        authorlist.append(authorname)

    for organ in organs:
        organname = organ.xpath('a/text()')[0]
        # print(organname)
        organlist.append(organname)
    authors = ','.join(authorlist)
    organs = ','.join(organlist)
    print(text, isbn, authors, organs)
    sql = """ INSERT INTO CNKI(title,isbn,author,organ,time) VALUES ('%s','%s','%s','%s','%s')""" % (text, isbn, authors, organs,sj)
    try:
        cursor.execute(sql)
        db.commit()
        print('successful')
    except:
        db.rollback()

start = time.time()

for i in range(1,73):
    url = 'http://nvsm.cnki.net/KNS/request/SearchHandler.ashx'
    s = requests.session()
    r = s.post(url, data=data, headers=headers)
    useragents = random.choice(users)
    headers = {
        'User-Agent': useragents,

    }

    url = 'http://nvsm.cnki.net/kns/brief/brief.aspx?curpage={}&RecordsPerPage=50&QueryID=3&ID=&turnpage=1&tpagemode=L&dbPrefix=SCDB&Fields=&DisplayMode=listmode&PageName=ASP.brief_result_aspx&isinEn=1&'.format(i)


    r = s.get(url,headers=headers)

    # print(r.text)
    e = etree.HTML(r.text)
    l = e.xpath('//*[@bgcolor]//td[5]')
    sj = []
    for x in l:
        k = x.xpath('text()')[0].strip()
        sj.append(k)
    print(url)
    n = re.findall(r'&FileName=(.*?)&', r.text)
    # if len(n) == 0:
    #     time.sleep(60)
    #     continue


    if len(sj)==0:
        # time.sleep(60)
        continue
    del sj[0]

    r.encoding='utf-8'

    dbname = re.findall(r'&DbName=(.*?)&',r.text)
    dbcode = re.findall(r'&DbCode=(.*?)&',r.text)
    zipp = list(zip(sj,n,dbname,dbcode))


    print(zipp)
    url2 = 'http://kns.cnki.net/KCMS/detail/detail.aspx?'
    urle = 'http://kns.cnki.net/KCMS/detail/detail.aspx?'
    for zipp in zipp:
        if len(zipp[1])<30:
            url3 = url2+'&dbcode='+zipp[3]+'&dbname='+zipp[2]+'&filename='+zipp[1]
            print(url3)
            try:
                pass
                parse_detail(url3,zipp[0])
            except:
                pass
        else:
            url3 = url2 + '&dbcode=' + zipp[3] + '&dbname=' + zipp[2] + '&filename=' + zipp[1]
            print(url3)
            try:
                pass
                parse_detaile(url3,zipp[0])
            except:
                pass


cursor.close()
db.close()
end = time.time()
ending= end - start

print('共用时'+str(ending)+'秒')

# e.xpath('//table[@class="GridTableContent"]/tbody/tr[@bgcolor]')
