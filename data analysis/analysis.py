# __author__ 08163318 韩志超
import sys
import matplotlib.pyplot as plt
import numpy as np
import csv
import re
import matplotlib
from wordcloud import WordCloud
import jieba
from PIL import Image

# 绘制饼状图
def paint_pie(recipe, data, title):
	fig, ax = plt.subplots(figsize=(8, 4), subplot_kw=dict(aspect="equal")) # 设置窗口大小
	wedges, texts = ax.pie(data, wedgeprops=dict(width=1), startangle=-40)

	bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
	kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
	          bbox=bbox_props, zorder=0, va="center")

	for i, p in enumerate(wedges):
	    ang = (p.theta2 - p.theta1)/2. + p.theta1
	    y = np.sin(np.deg2rad(ang))
	    x = np.cos(np.deg2rad(ang))
	    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
	    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
	    kw["arrowprops"].update({"connectionstyle": connectionstyle})
	    ax.annotate(recipe[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
	                 horizontalalignment=horizontalalignment, **kw)
	ax.set_title(title)
	plt.show()


# 绘制词云
def paint_wd(cloudtext,filename):
	stopwords = [
		'如何', '为什么', '什么', '输入', '输出', '修改', '怎么', '在线', 'to', '查看', '实现', 'not', '一个', '没有', '世界', '可以'
	]# 屏蔽掉一些无用的词
	bg=np.array(Image.open("bg.jfif")) # 背景图片
	wc = WordCloud(
		background_color="white",
		max_words=500,
		font_path='C:/Windows/Fonts/simkai.ttf',
		min_font_size=15,
    	max_font_size=80, 
    	width = 400,
    	stopwords = stopwords,
    	mask = bg
	)
	wc.generate(cloudtext)
	wc.to_file(filename)


# 绘制折线图
def paint_linechart(x, y, x_name, y_name, title):
	plt.plot(x, y)
	plt.xticks()
	plt.xlabel(x_name)
	plt.ylabel(y_name)
	plt.title(title)
	plt.show()


# 命令封装
args = sys.argv
if len(args) < 2:
	output = """
usage: python annlysis.py file graph.
file: your csv file.
graph: [pie, wordcloud, linechart]
		"""
	print(output)
	exit()
else:
	csvfile = args[1]



# 数据预处理

domains = dict()

vi_types = dict()

keywords = dict()

times = dict()

with open("chrome.csv",'r') as file:
	lines = csv.reader(file)
	next(lines) # 去掉第一行
	for line in lines:
		# 统计上网时间
		tmp_time = re.search(r'([0-9]+:[0-9]+)', line[2]).group(1)
		tmp_time = tmp_time.split(':')[0]
		if tmp_time not in times.keys():
			times[tmp_time] = 1
		else:
			times[tmp_time] += 1

		# 统计域名
		name = re.search(r'http[s]{0,1}://(([0-9a-z]|\.|\-)+)',line[0])
		tmp_type = line[5]
		if name == None:
			continue
		name = name.group(1)
		if name not in domains.keys():
			domains[name] = 1
		else:
			domains[name] += 1

		if tmp_type not in vi_types.keys():
			vi_types[tmp_type] = 1
		else:
			vi_types[tmp_type] += 1

		# 统计关键词
		tmp_word = re.search(r'(.+)(_百度搜索| \- Google Search)', line[1])
		if tmp_word == None:
			continue
		tmp_word = tmp_word.group(1)
		if tmp_word not in keywords.keys():
			keywords[tmp_word] = 1
		else:
			keywords[tmp_word] += 1

		
	
	# print(times)
	# print(len(times))
	# print(sum(times.values()))
	


# 域名数据处理，去除baidu,xiaoyuanwagndegnlu,google
blacklist = ['10.2.5.251','www.baidu.com','www.google.com.hk','127.0.0.1','www.google.com','192.168.75.133',
	'192.168.1.100','i.g-fox.cn','home.firefoxchina.cn']
for item in blacklist:
	if item in domains.keys():
		domains.pop(item)
sorted_domains = sorted(domains.items(),key=lambda x: x[1],reverse=True)
recipe = [i[0] for i in sorted_domains][:25]
data = [i[1] for i in sorted_domains][:25]


# 关键词数据处理，利用jieba库将中文分词
text = ','.join(keywords.keys())
segs = jieba.cut(text)
new_text = []
for seg in segs:
	if seg != ',' and seg != "" and len(seg)!=1:
		new_text.append(seg.replace(" ",""))

text = ",".join(new_text)


# 浏览时间数据处理

# 补全前几个小时使得线段看起来平滑
for i in range(0,24,2):
	if str(i) not in times.keys():
		times[str(i)] = 0

sorted_times = sorted(times.items(),key=lambda x: int(x[0]),reverse=False)
x = [i[0] for i in sorted_times]
x = x[2:] + x[:2]
y = [i[1] for i in sorted_times]
y = y[2:] + y[:2]
xname = 'time'
yname = 'visit count'
title = 'Map of Internet time'



# 命令封装
for i in range(2,len(args)):
		if "pie" == args[i]:
			paint_pie(recipe,data,'Network access distribution map')
		elif "wordcloud" == args[i]:
			paint_wd(text, 'wordcloud.png')
			print("File was stored as wordcloud.png")
		elif "linechart" == args[i]:
			paint_linechart(x, y, xname, yname, title)




# paint_pie(recipe,data,'Network access distribution map')

# paint_wd(text, 'wordcloud.png')

# paint_linechart(x, y, xname, yname, title)
