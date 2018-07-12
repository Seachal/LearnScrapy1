# -*- coding: utf-8 -*-

import scrapy


class BooksSpider(scrapy.Spider):
    # 每一个爬虫的唯一标识

    name = "books"  #声明变量

    # 定义爬虫爬取的起始点，起始点可以是多个，这里只有一个

    start_urls = ['http://books.toscrape.com/'] # 声明列表

    def parse(self, response):

        # 提取数据

        # 每一本书的信息在<article class="product_ pod“>中，我们使用

        # css（）方法找到所有这样的 article 元素，并依次迭代

        for book in response.css('article.product_pod'):

            # 书名信息在 article> h3> a 元素的 title 属性里
            #  #例如： <a title="A Light in the Attic"> A Light In the... < / a >

            name = book.xpath('./h3/a/@title').extract_first()

            # 书价信息在《p class="price_. Color“》的 TEXT 中。
            #  例如： <p class="price_ color">f51.77</p>

            price = book.css('p.price_color::text').extract_first()

# 声明字典？
            yield {
                'name': name,
                'price': price,
            }

            # 提取链接

            # 下一页的 url 在 ul. Pager> li. Next> a 里面
            # #例如： <li class="next"> <a href="catalogue/ page-2. html">next</a></li>

            next_url = response.css('ul.pager li.next a::attr (href) ').extract_first()

            if next_url:
                # 如果找到下一页的 URL，得到绝对路径，构造新的 Request 对象

                next_url = response.urljoin(next_url)
                yield scrapy.Request(next_url, callback=self.parse)
