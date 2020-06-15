import csv
import matplotlib.pyplot as plt
from datetime import datetime


# 从文件中获取最高气温 最低气温
filename = 'dataset/sitka_weather_2014.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader) # next()返回文件的下一行，只调用了next（）一次，则得到的是文件的第一行

    for index, column_header in enumerate(header_row):
        print(index, column_header)

    dates, highs, lows = [], [], []
    for row in reader:
        try:
            # 错误预知,避免出现有些部分没有数据
            current_date = datetime.strptime(row[0], '%Y-%m-%d')  # 使用strptime（）将字符串日期转化为标准显示日期
            high = int(row[1])
            low = int(row[3])
        except ValueError:
            print(current_date, 'missing date')
        else:
            highs.append(int(row[1]))
            lows.append(int(row[3]))
            dates.append(current_date)

fig = plt.figure(dpi=128, figsize=(10, 6))
plot1 = plt.plot(dates, highs, c='red', alpha=0.5) # alpha指定颜色透明度
plot2 = plt.plot(dates, lows, c='blue', alpha=0.5) # 注意dates和highs 以及lows是匹配对应的
plt.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1) # facecolor指定了区域的颜色

# 设置图形格式
plt.title("Daily high and low temperature, 2014", fontsize=24)
plt.xlabel('', fontsize=14)
fig.autofmt_xdate() # 让x轴标签斜着打印避免拥挤
plt.ylabel('Temperature(F)', fontsize=14)
plt.tick_params(axis='both', which='major', labelsize=14)

plt.legend()
plt.show()
