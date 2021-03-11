import scrapy
import json

class HipsterSpider(scrapy.Spider):
    name = 'hipster'
    start_urls = ['http://34.64.171.117:8080/#/']
    
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': '34.64.171.117:8080',
        'Origin': 'http://34.64.171.117:8080/',
        'Pragma': 'no-cache',
        'Referer': 'http://34.64.171.117:8080/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    }

    def parse(self, response):
        url = 'http://34.64.171.117:8080/api/products'

        yield scrapy.Request(url, callback=self.parse_api, headers=self.headers)


    def parse_api(self, response):
        base_url = 'http://34.64.171.117:8080/api/products?ids='

        raw_data = response.body
        data = json.loads(raw_data)

        print('data'+'*' * 20)
        print(data) 
        print('*' * 20)

        prdts = data['products']

        for prdt in prdts:
            prdt_id = prdt['id']
            prdt_url = base_url + prdt_id

            request = scrapy.Request(prdt_url, callback=self.parse_product, headers=self.headers)
            yield request


    def parse_product(self, response):
        raw_data = response.body
        data = json.loads(raw_data)

        prdt = data['products'][0]
        
        yield {
            'Name' : prdt['name'],
            'Image' : prdt['picture'],
            "Description" : prdt['description'],
            'Currency' : prdt['priceUsd']['currencyCode'],
            'Units': prdt['priceUsd']['units'],
            'nanos' : prdt['priceUsd']['nanos']
        }
