import pymysql
import csv
import re


db = pymysql.connect('127.0.0.1','root','root','tongxun',charset='utf8')

cursor = db.cursor()

def insert(data):
    sql = "INSERT INTO stuinfo VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    tmp = []
    for it in data:
        tmp.append(it.encode('utf-8'))
    para = tuple(tmp)
    cursor.execute(sql,para)
    db.commit()


def search(num,keyword,job):
    if keyword == "":
        if job == '全部':
            sql = "select * from stuinfo;"
        else:
            sql = "select * from stuinfo where 专业='"+job+"';"
    else:
        if job == '全部':
            if keyword.isdigit():
                sql = "select * from stuinfo where 手机号码 like '%" + keyword + "%';"
            else:
                sql = "select * from stuinfo where 姓名 like '%" + keyword + "%';"
        else:
            if keyword.isdigit():
                sql = "select * from stuinfo where 手机号码 like '%" + keyword + "%' and 专业='" + job + "';"
            else:
                sql = "select * from stuinfo where 姓名 like '%" + keyword + "%' and 专业='" + job + "';"
    cursor.execute(sql)
    return cursor.fetchall()
    # if num == 1:
    #     if job == '全部':
    #         sql = "select * from stuinfo where 姓名='" + keyword + "';"
    #     else:
    #         sql = "select * from stuinfo where 姓名='"+keyword+"' and 专业='"+job+"';"
    #     cursor.execute(sql)
    #     return cursor.fetchall()
    # if num == 2:
    #     if job == '全部':
    #         sql = "select * from stuinfo where 手机号码='" + keyword + "';"
    #     else:
    #         sql = "select * from stuinfo where 手机号码='"+keyword+"' and 专业='"+job+"';"
    #     cursor.execute(sql)
    #     return cursor.fetchall()
    # if num == 0:
    #     if job == '全部':
    #         sql = "select * from stuinfo where 编号='" + keyword + "';"
    #     else:
    #         sql = "select * from stuinfo where 编号='" + keyword + "' and 专业='" + job + "';"

        # cursor.execute(sql)
        # return cursor.fetchall()    


# def search(num,keyword,job):
#     if keyword == "":
#         if job == '全部':
#             sql = "select * from stuinfo;"
#         else:
#             sql = "select * from stuinfo where 专业='"+job+"';"
#         cursor.execute(sql)
#         return cursor.fetchall()
#     if num == 1:
#         if job == '全部':
#             sql = "select * from stuinfo where 姓名='" + keyword + "';"
#         else:
#             sql = "select * from stuinfo where 姓名='"+keyword+"' and 专业='"+job+"';"
#         cursor.execute(sql)
#         return cursor.fetchall()
#     if num == 2:
#         if job == '全部':
#             sql = "select * from stuinfo where 手机号码='" + keyword + "';"
#         else:
#             sql = "select * from stuinfo where 手机号码='"+keyword+"' and 专业='"+job+"';"
#         cursor.execute(sql)
#         return cursor.fetchall()
#     if num == 0:
#         if job == '全部':
#             sql = "select * from stuinfo where 编号='" + keyword + "';"
#         else:
#             sql = "select * from stuinfo where 编号='" + keyword + "' and 专业='" + job + "';"
#         cursor.execute(sql)
#         return cursor.fetchall()

def delete(data):
    sql = "delete from stuinfo where 编号='"+data+"';"
    cursor.execute(sql)
    db.commit()

def restore(filename):
    sql = "truncate table stuinfo;"
    cursor.execute(sql)
    db.commit()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == '学生编号':
                continue
            insert(row)

def edit(data):
    sql = "delete from stuinfo where 编号='"+data[0]+"';"
    cursor.execute(sql)
    insert(data)

def filltable(index):
    if index == '全部':
        sql = "select * from stuinfo;"
    else:
        sql = "select * from stuinfo where 专业='"+index+"';"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
