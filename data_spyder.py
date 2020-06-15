import requests
from bs4 import BeautifulSoup
from pyecharts import Bar
ALL_DATA = []
def parse_page(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    text = response.content.decode('utf-8')
    # html5ilb有很高的容错性，如果有标签缺失，它就会自动补齐
    # pip install html5lib
    soup = BeautifulSoup(text,'html5lib')
    conMidtab = soup.find('div',class_='conMidtab')
    tables = conMidtab.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]
        for index,tr in enumerate(trs):
            tds = tr.find_all('td')
            # 获取城市
            city_td = tds[0]
            # 获取最低气温
            temp_td = tds[-2]
            # 获取天气状况
            weather_td = tds[1]
            if index == 0:
                city_td = tds[1]
                weather_td = tds[2]
            city = list(city_td.stripped_strings)[0]
            min_temp = list(temp_td.stripped_strings)[0]
            weather = list(weather_td.stripped_strings)[0]
            ALL_DATA.append({"city":city,"min_temp":int(min_temp),"weather":weather})
            # print({"city":city,"min_temp":int(min_temp),"weather":weather})


def main():
#   创建url池，表示不同地区的url
    urls = [
        'http://www.weather.com.cn/textFC/hb.shtml',
        'http://www.weather.com.cn/textFC/db.shtml',
        'http://www.weather.com.cn/textFC/hd.shtml',
        'http://www.weather.com.cn/textFC/hz.shtml',
        'http://www.weather.com.cn/textFC/hn.shtml',
        'http://www.weather.com.cn/textFC/xb.shtml',
        'http://www.weather.com.cn/textFC/xn.shtml',
        'http://www.weather.com.cn/textFC/gat.shtml'
    ]
    for url in urls:
        parse_page(url)

    # 根据最低气温进行排序
    ALL_DATA.sort(key=lambda data:data['min_temp'])
    data= ALL_DATA[0:10]
    cities = list(map(lambda x:x['city'],data))
    temps = list(map(lambda x:x['min_temp'],data))
    # 取前面十个
#     可视化pyecharts pip install pyecharts
#     但是目前的pyecharts与1.0版本一下的不一样，有一些方法不同，需要还原为0.1.9.4
    chart = Bar('中国最低气温')
    chart.add('',cities,temps)
    chart.render('temperature.html')


if __name__ == '__main__':
    main()

