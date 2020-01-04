# 简介

本项目是业余时间写的一些python相关的小项目

## 通讯录

一个基于tkinter的图形界面项目，实现了通讯录的增删改查、备份与恢复等功能，支持mysql数据库来存储数据或用csv格式，在程序中通过db_open 变量来控制是否启用数据库

运行效果如下

![3@9D1ZRB_EPHY8LU15_11MC.png](https://i.loli.net/2020/01/04/yiW7hwbX5cfCaDN.png)

## 数据分析

通过提取浏览器数据进行数据分析，绘出域名占比饼状图，搜索关键词词云，每天不同时段上网频率变化趋势图

>usage: python annlysis.py file graph.
file: your csv file.
graph: [pie, wordcloud, linechart]

PS：chrome浏览器浏览记录本身就是以数据库形式存储，直接提取即可，firefox浏览器等浏览记录数据可以通过一些提取软件来提取，存储格式为csv格式

运行效果

![8~_CBUVX1D8AHD_9CA_I~KS.png](https://i.loli.net/2020/01/04/ioMFr83SzXuA9wa.png)


![KEV58NW~FMK_QW2_7SBLMZ8.png](https://i.loli.net/2020/01/04/oAci2HwYVaektXx.png)

