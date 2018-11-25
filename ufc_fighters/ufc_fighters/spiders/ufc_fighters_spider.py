import scrapy
import string
from datetime import datetime
from scrapy.loader import ItemLoader
from ufc_fighters.items import UfcFighterItem


class UfcFighterSpider(scrapy.Spider):
    """Scrape fightmetric.com for every ufc event"""
    name = "ufc_fighter"
    allowed_domains = ["fightmetric.com"]

    # construct web addresses that need to be visited

    start_urls = ["http://www.fightmetric.com/statistics/fighters?char="+\
                l + "&page=all" for l in string.ascii_lowercase]

    # for debug purposes:
    # start_urls = ["http://www.fightmetric.com/fighter-details/f57a8a52ca401ed9"]
    
    def parse(self, response):
        """follow each each fighter to get his/her statistics"""

        # follow each fighter
        for sel in response.xpath("//table[@class='b-statistics__table']" +
            "/tbody/tr[@class='b-statistics__table-row']"):
            fighter_href = sel.xpath(".//td[@class='b-statistics__table-col']" +\
                "/a/@href").extract_first()

            if fighter_href is not None:
                yield response.follow(fighter_href, callback=self.parse_fighter)

    def parse_fighter(self, response):
        """For each fighter grab info and career statistics."""
        info = {}

        fighter_name = response.xpath("//h2[@class='b-content__title']" +
            "/span[@class='b-content__title-highlight']/text()").extract_first().strip()
        info["name"] = fighter_name

        record = response.xpath("//h2[@class='b-content__title']" +
            "/span[@class='b-content__title-record']/text()").extract_first().strip()

        # split recort into win, lose, and draw, and nc if applicable
        record = record.split(": ")[1]
        w_l_d = record.split("-")

        info["win"] = w_l_d[0]
        info["lose"] = w_l_d[1]

        if w_l_d[2].find("(") == -1:
            info["draw"] = w_l_d[2]
            info["nc"] = "0"
        else:
            info["draw"] = w_l_d[2][:w_l_d[2].find("(") - 1]
            # no contest
            info["nc"] = w_l_d[2][w_l_d[2].find("(") + 1: ].split()[0]

        for sel in response.xpath("//div[@class='b-list__info-box " +
            "b-list__info-box_style_small-width js-guide']" +
            "/ul[@class='b-list__box-list']/li"):
            item = sel.xpath(".//i/text()").extract_first()

            # remove character :
            item = item.strip().lower()[:-1]

            if item:
                item_value_sel = sel.xpath("text()")
                
                # be careful of "\n"
                if item_value_sel:
                    item_value = item_value_sel.extract()[-1].strip()

                    # use empty string for missing information
                    info[item] = item_value if item_value != "--" else "N/A"        
                else:
                    info[item] = "N/A"

        # for debug
        #print(info)

        # career statistics
        stat = {}
        for sel in response.xpath("//div[@class='b-list__info-box-left clearfix']/div" +
            "/ul[@class='b-list__box-list b-list__box-list_margin-top']/li"):
            item = sel.xpath(".//i/text()").extract_first()

            # remove character :
            item = item.strip()[:-1]

            # modify variable names
            item = item.replace(".", "").replace(" ", "_")

            if item:
                item_value_sel = sel.xpath("text()")
                
                # be careful of "\n"
                if item_value_sel:
                    item_value = item_value_sel.extract()[-1].strip()
                    stat[item] = item_value
                else:
                    stat[item] = "N/A"
        # for debug
        # print(info)
        # print(stat)

        # use loader to populate items
        loader = ItemLoader(item=UfcFighterItem(), response=response)

        for d in[info, stat]:
            for k, v in d.items():
                loader.add_value(k, v)
        
        loader.add_value("last_updated", datetime.now())
        
        # yield each matach as an item
        ufc_fighter_item = loader.load_item()
        yield ufc_fighter_item
