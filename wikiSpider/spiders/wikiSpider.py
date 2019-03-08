# -*- coding: utf-8 -*-
import scrapy
from wikiSpider.items import WikispiderItem
import re
   

BASE_URL = 'http://en.wikipedia.org'


class wikiSpider(scrapy.Spider):
# spider for wikipedia "2018 FIFA World Cup Player
    name = '2018_fifa'
    allowed_domains = ['en.wikipedia.org']
    start_urls = [
        "https://en.wikipedia.org/wiki/2018_FIFA_World_Cup_squads"
    ]

    def parse(self,response):
        self.log("processing: %s" % response.url)

        h3s = response.xpath('//h3') # obtain all <h3> headders (team country names) on the page
        for h3 in h3s:
            country = h3.xpath('span[@class="mw-headline"]/text()').extract()
            self.log("processing: %s" % country)
            
            tables = h3.xpath('following-sibling::table[1]/tbody') # obtain table the sibling value of mw-headline
            if tables:
                self.log("processing: table")
                #print(tables)

                for t in tables.xpath('tr[@class="nat-fs-player"]'): 
                    self.log("processing: rows")
                    table_data = process_player_data(t, country[0])

                    request = scrapy.Request(   
                        url = table_data['link'],            # use link from process_player_data
                        callback=self.parse_bio,       # setting callback to process the response
                        dont_filter=True)
                    request.meta['item'] = WikispiderItem(**table_data)
                    print("request={0}".format(request.meta))
                                             
                    yield request  
                
                    #yield table_data
            



    def parse_bio(self, response):
        print(response.meta)
        item = response.meta['item']
        href = response.xpath("//li[@id='t-wikibase']/a/@href").extract()
        
        if href:
            request = scrapy.Request(href[0], callback=self.parse_wikidata, dont_filter=True)
                        
            request.meta['item'] = item
            yield request
            


    def parse_wikidata(self, response):
        self.log("processing: wikiitems")
        print(response.meta)
        item = response.meta['item']

        property_codes = [ 
            {'name': 'citizenship', 'code':'P27', 'link':True},
            {'name':'mass', 'code':'P2067'},
            #{'name':'participated', 'code':'P1344', 'link':True},
            {'name':'height', 'code':'P2048'},
            {'name':'FIFAID', 'code':'P1469', 'link':True},
            {'name':'TransferMKT_ID', 'code':'P2446', 'link':True}
        ]

        # list: country of citizenship P27,
        # mass P2067, 
        # participant of P1344, 
        # height P2048, 
        # 'TransferMKT_ID', 'code':'P2446'
        # FIFA palayer ID P1469

        #p_template = '//*[@id="{code}"]/div[2]/div[1]/div/div[2]/div[2]{link_html}/text()'

        p_template = '//*[@id="{code}"]/div[2]/div/div/div[2]/div[1]/div/div[2]/div[2]{link_html}/text()'

        for prop in property_codes:
            
            link_html = '/div[1]'
            if prop.get('link'):
                link_html = '/div[1]/a'
            sel = response.xpath(p_template.format( \
                code=prop['code'], link_html=link_html)) 
            if sel:
                item[prop['name']] = sel[0].extract()
        print(item)
        self.log("done: wikiitems")
        yield item

        

        # //*[@id="P1469"]
        # //*[@id="Q523640$523453D6-D12C-4DC3-817B-EE65A76E7417"]/div[2]/div[1]/div/div[2]/div[2]/div[1]/a
        # //*[@id="Q523640$F7F66C65-D21F-4F69-A5ED-7E947F390D5E"]/div[2]/div[1]/div/div[2]/div[2]/div[1]/text()
        # //*[@id="Q523640$3A5A36D1-DA56-41E2-8172-491CD41AD56C"]/div[2]/div[1]/div/div[2]/div[2]/div[1]/a
        # //*[@id="Q523640$39DF235E-9F99-4AF1-84DE-7EEDE83B6FBA"]/div[2]/div[1]/div/div[2]/div[2]/div[1]/text()
        # //*[@id="Q523640$B0524EA7-FD92-44C6-AE92-5D20170276BC"]/div[2]/div[1]/div/div[2]/div[2]/div[1]/a
        # //*[@id="Q523640$1391CF25-149A-4A39-BB97-115457DF1CF7"]/div[2]/div[1]/div/div[2]/div[2]/div[1]/a
        # //*[@id="q155525$82312275-D23F-4048-A710-6EC6AB12C2C2"]/div[2]/div[1]/div/div[2]/div[2]/div[1]/text()




def process_player_data(t, country=None):
    """
    process the table tags <td>, <th>
    and add his team country name

    """

    table_data = {}
    table_data['name'] = t.xpath('th[1]/a/text()').extract()[0]
    table_data['link'] = BASE_URL + t.xpath('th/a/@href').extract()[0]
    table_data['numb'] = t.xpath('td[1]/text()').extract()[0]
    table_data['position'] = t.xpath('td[2]/a/text()').extract()[0]
    table_data['DOB'] = t.xpath('td[3]/span/span[@class="bday"]/text()').extract()[0]
    table_data['caps'] = t.xpath('td[4]/text()').extract()[0]
    table_data['goals'] = t.xpath('td[5]/text()').extract()[0]
    table_data['club'] = t.xpath('td[6]/a/text()').extract()[0]
    table_data['team'] = country



    return table_data




