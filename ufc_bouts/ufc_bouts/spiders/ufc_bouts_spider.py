import scrapy
from datetime import datetime
from scrapy.loader import ItemLoader
from ufc_bouts.items import UfcBoutItem


class UfcBoutSpider(scrapy.Spider):
    """Scrape fightmetric.com for every ufc event"""
    name = "ufc_bout"
    allowed_domains = ["fightmetric.com"]

    # construct web addresses that need to be visited
    start_urls = ["http://www.fightmetric.com/statistics/events/completed?page=all"]
    
    def parse(self, response):
        """follow each event to get bout details"""

        # follow each event
        for event_href in response.xpath("//tr[@class='b-statistics__table-row']" +
            "/td[@class='b-statistics__table-col']" +
            "/i[@class='b-statistics__table-content']/a/@href"):
            yield response.follow(event_href, callback=self.parse_event)

        # for debug purposes
        # yield scrapy.Request("http://www.fightmetric.com/event-details/20e403a1acfef130",
        #     self.parse_event)

    def parse_event(self, response):
        """For event info and bout results for each event."""

        # event name
        event_name = response.xpath("//h2[@class='b-content__title']" +
            "/span[@class='b-content__title-highlight']/text()").extract_first().strip()
        
        # event_date, location, attendance
        date_loc_atten = {}
        for sel in response.xpath("//li[@class='b-list__box-list-item']"):
            item_name = sel.xpath(".//i/text()").extract_first()
            # remove : at the end
            item_name = item_name.strip().lower()[:-1]

            item_value_sel = sel.xpath("text()")

            # be careful of "\n"
            if item_value_sel:
                item_value = item_value_sel.extract()[-1].strip()

            if item_name == "date":
                item_value = datetime.strptime(item_value , '%B %d, %Y').date()

            # change attendance to int
            if item_name == "attendance":
                if item_value:
                    item_value = int(item_value.replace(",", ""))

            date_loc_atten[item_name] = item_value
        
        # results of each match
        for sel in response.xpath("//tr[@class='b-fight-details__table-row" +
            " b-fight-details__table-row__hover js-fight-details-click']"):

            # use loader to populate items
            loader = ItemLoader(item=UfcBoutItem(), response=response)

            # load event_name, date, location, and attendance
            loader.add_value("event_name", event_name)
            
            for k, v in date_loc_atten.items():
                loader.add_value(k, v)

            # get table columns
            columns = sel.xpath(".//td")

            # column 1 - win or lose
            result = columns[0].xpath(".//i[@class='b-flag__text']/text()").extract_first().strip()
            loader.add_value("result", result)

            # for winner
            win = True if result == "win" else False

            # column 2 - fighter
            fighters = columns[1].xpath(".//p/a/text()").extract()
            loader.add_value("fighter1", fighters[0].strip())            
            loader.add_value("fighter2", fighters[1].strip())
            
            # they always show winners first if there is one
            winner = fighters[0].strip() if win else ""
            loader.add_value("winner", winner)

            # column 7 - weight class
            weight_class = columns[6].xpath(".//p/text()").extract_first().strip()
            loader.add_value("weight_class", weight_class)
            
            # whether it was a title fight
            title_fight_sel = columns[6].xpath(".//p/img[contains(@src, 'belt')]")
            title_fight = True if title_fight_sel else False
            loader.add_value("title_fight", title_fight)

            # column 8 - match finishing method
            method = columns[7].xpath(".//p/text()").extract()
            method = [m.strip() for m in method]

            # modify the format of decisions
            if method[0] == "M-DEC":
                method[0] = "DEC-Majority"
            elif method[0] == "U-DEC":
                method[0] = "DEC-Unanimous"
            elif method[0] == "S-DEC":
                method[0] = "DEC-Split"

            method = "-".join(method) if method[1] else method[0]
            loader.add_value("method", method)

            # columns 9 and 10 - finishing round and time
            end_round = columns[8].xpath(".//p/text()").extract_first().strip()
            end_round = int(end_round)
            loader.add_value("end_round", end_round)

            end_time = columns[9].xpath(".//p/text()").extract_first().strip()
            loader.add_value("end_time", end_time)

            # yield each matach as an item
            ufc_bout_item = loader.load_item()
            yield ufc_bout_item