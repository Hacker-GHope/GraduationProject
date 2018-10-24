# -*- coding: utf-8 -*-
# @Time    : 2018/10/24 16:10
# @Author  : G.Hope
# @Email   : 1638327522@qq.com
# @File    : Spider_58Ershoufang.py
# @Software: PyCharm

import pymysql
import requests

from lxml import etree


# 获取网页
def get_html(url):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        text = response.content.decode('utf-8')
        return text
    return None


# 解析网页内容
def parse_html(html):
    # 创建解析对象
    etree_html = etree.HTML(html)
    # 解析标题
    house_title = etree_html.xpath('//div[@class="list-info"]/h2/a/text()')
    # print(house_title)
    # 解析地址
    house_local = etree_html.xpath('//div[@class="list-info"]/p/span/a/text()')
    # print(house_local)
    # 解析详细信息
    house_details = etree_html.xpath('//div[@class="list-info"]/p/span/text()')
    # print(house_details)
    # 解析价格
    house_price = etree_html.xpath('//div[@class="price"]/p[@class="unit"]/text()')
    # print(house_price)
    # 图片地址
    house_img = etree_html.xpath('//div[@class="pic"]/a/img/@src')
    # print(house_img)
    # 经济人
    # 网页中存在经济人、个人和独立经济人三种所有者，不能对齐，所以暂且省略
    # house_houseman = etree_html.xpath('//div[@class="jjrinfo"]/a/span/text()')
    # print(house_houseman)
    # 链接
    house_link = etree_html.xpath('//div[@class="list-info"]/h2/a/@href')
    # print(house_link)
    # 唯一索引
    # house_ux = etree_html.xpath('//div[@class="content-side-left"}/ul/li/@logr')
    # print(house_ux)
    items = []
    for i in range(len(house_img)):
        item = {}
        item['title'] = house_title[i].strip()
        item['local'] = house_local[i]
        item['details'] = house_details[i].strip()
        item['price'] = house_price[i]
        item['img'] = house_img[i]
        # item['houseman'] = house_houseman[i]
        item['link'] = house_link[i]
        # item['ux'] = house_ux[i]
        items.append(item)
    return items


# 保存内容到数据库中
def join_mysql(items):
    # 设置数据库参数
    host = '127.0.0.1'
    user = 'root'
    password = 'root'
    port = 3306
    db = 'house'
    db = pymysql.connect(host=host, user=user, password=password, port=port, db=db)
    # 连接数据库
    cursor = db.cursor()
    for i in range(len(items)):
        sql = "INSERT INTO city(title,local,details,price,img,link)" \
              " VALUES('{}','{}','{}','{}','{}','{}')".format(items[i]['title'],
              items[i]['local'],items[i]['details'],items[i]['price'],items[i]['img'],items[i]['link'])
        # print(sql)
        cursor.execute(sql)
        db.commit()
    db.close()


def main():
    for i in range(1, 71):
        if i == 1:
            url = 'https://panzhihua.58.com/ershoufang/?PGTID=0d30000c-0094-3ff2-cf38-210e5987b783&ClickID=1'
        else:
            url = 'https://panzhihua.58.com/ershoufang/pn' + str(
                i) + '/?PGTID=0d30000c-0094-3ff2-cf38-210e5987b783&ClickID=1'
        html = get_html(url)
        # print(html)
        items = parse_html(html)
        # print(items)
        join_mysql(items)


if __name__ == '__main__':
    main()
