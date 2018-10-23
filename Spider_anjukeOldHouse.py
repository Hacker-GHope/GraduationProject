# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 17:21
# @Author  : G.Hope
# @Email   : 1638327522@qq.com
# @File    : Spider_anjukeOldHouse.py
# @Software: PyCharm
import json

import requests
from bs4 import BeautifulSoup


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


# 解析页面
def parse_soup(html):
    soup = BeautifulSoup(html,'lxml')
    # 解析图片地址
    result = soup.select('.item-img img')
    # print(result)
    house_image = result
    # 解析房屋信息
    result = soup.select('.house-details .details-item')
    # print(result)
    house_details = result
    # 解析价格信息
    result = soup.select('.pro-price .unit-price')
    # print(result)
    house_price = result
    house = []
    for i in range(len(house_image)):
        item = {}
        item['img'] = house_image[i].attrs['src']
        item['details'] = house_details[i].text
        item['price'] = house_price[i].text
        house.append(item)
    return house


# 保存图片
def write_image(local):
    for i in range(len(local)):
        url_parts = local[i]['img']
        filename = "./安居客/images/%s.jpg" % url_parts.split("//")[-1].split('/')[-1].split('?')
        r = requests.get(url_parts)
        with open(filename, "wb") as f:
            f.write(r.content)

# 写入数据
def write_json(items):
    house_json = json.dumps(items, ensure_ascii=False, check_circular=True)
    filename = './安居客/安居客二手房信息'
    with open(filename, "a", encoding='utf-8') as f:
        f.write(house_json)

# 主程序
def main():
    # url = 'https://panzhihua.anjuke.com/sale/p1/#filtersort'
    # html = get_html(url)
    # items = parse_soup(html)
    # write_json(items)
    # write_image(items)
    for i in range(50):
        url = 'https://panzhihua.anjuke.com/sale/p'+str(i)+'/#filtersort'
        html = get_html(url)
        items = parse_soup(html)
        # write_json(items)
        write_image(items)


if __name__ == '__main__':
    main()