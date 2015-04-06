# -*- coding: utf-8 -*-
import urlparse
import re
from datetime import datetime

from scrapy import Request, Spider
from scrapy import log
from rpost.items import RacedayItemLoader

from rpost.items import HorseItem
import re
import pprint


def imperialweighttokg(imperialweight):
    """stone ounces """
    if "-" not in imperialweight or imperialweight is None:
        return None
    else:
        stones, pounds = imperialweight.split("-")
        return round(((int(stones) * 14) + int(pounds)) / 2.20462262, 0)


class RacingPostSpider(Spider):
    log.msg("Spider for racingpost started", level=log.INFO)
    name = "racing_old"

    allowed_domains = ["racingpost.com", "pedigreequery.com"]

    start_urls = [
        "http://www.racingpost.com/horses2/cards/home.sd?r_date={today}".format(
            today=datetime.today().strftime("%Y-%m-%d")
        )
        # 'http://www.racingpost.com/horses2/cards/card.sd?race_id=622916&r_date=2015-04-06#raceTabs=sc_',
    ]

    main_url = "http://www.racingpost.com"

    handle_httpstatus_list = [404, 403]

    def parse(self, response):
        """
        We parse the race cards list pages, and extract all the race cards urls
        """
        # relevant racecourses:
        # item_loader = RacedayItemLoader(item=HorseItem(), response=response)
        # todaysvenues = dict()

        # rcs = response.xpath("//td[@class='meeting']/h3[not(contains(., 'WORLDWIDE STAKES RACES')) and not(contains(.,'(AUS)')) and not(contains(., ' SCOOP6 RACES' )) ]/a/text()").extract()

        # goings = response.xpath("//td[@class='meeting']/h3[not(contains(., 'WORLDWIDE STAKES RACES')) and not(contains(.,'(AUS)')) and not(contains(., ' SCOOP6 RACES' )) ]/following::p[descendant::strong[contains(., 'GOING:')]]/text()").extract()
        # todaysvenues= dict(zip(rcs, goings))
        # pprint.pprint(todaysvenues)

        # for i, tr in enumerate(response.xpath("//td[@class='meeting']/h3[not(contains(., 'WORLDWIDE STAKES RACES')) and not(contains(.,'(AUS)')) and not(contains(., ' SCOOP6 RACES' )) ]")):
        # print tr.xpath('.//a[%s]/text()' % str(i)).extract()
        #     print tr.xpath(".//following::p[descendant::strong[contains(., 'GOING:')] and contains(@class, 'border')  ]/text()").extract() 

        # improved version excludes AUS and Scoop6
        # for href in response.xpath("//td[@class='crd bull']/a/@href[preceding::h3[not(contains(., 'WORLDWIDE STAKES RACES'))  and not(contains(.,'(AUS)')) and not(contains(., ' SCOOP6 RACES' ))        ]]").extract():
        for href in response.xpath("//td[@class='crd bull']/a/@href").extract():
            request = Request(
                re.sub(r'card\.sd', 'card_verdict.sd', urlparse.urljoin(self.main_url, href)),
                callback=self.parse_diomed
            )
            yield request

    def parse_diomed(self, response):

        item_loader = RacedayItemLoader(item=HorseItem(), response=response)
        item_loader.add_xpath('diomed', "//div[@id='diomed_verdict']//text()")
        return Request(
            re.sub(r'card_verdict\.sd', 'card.sd', response.url),
            meta={
                'item': item_loader.load_item()
            },
            callback=self.parse_race_card
        )

    def parse_race_card(self, response):
        """
        We parse the race card, and extract the race information and the horse card url
        """

        race_course = response.xpath("//span[contains(@class,'placeRace')]/text()").extract()
        race_name = response.xpath("(//div[@class='info']/p)[1]//text()").extract()
        race_class = response.xpath("(//div[@class='info']/p)[1]//text()").extract()
        race_time = response.xpath("//span[@class='navRace']/span/text()").extract()
        # from response.body
        race_date = response.xpath("//span[@class='date']/text()").extract()
        race_pm = response.xpath("p[@id=raceConditionsText]/text()").extract()
        # response.xpath("//div[@class='leftColBig']/ul/li/text()")

        # //*[text()[contains(.,'ABC')]]
        race_distance = response.xpath("//li[text()[contains(., 'Distance')]]/strong/text()").extract()
        race_going = response.xpath("//li[text()[contains(., 'Going:')]]/strong/text()").extract()
        # or from response.url
        race_date = re.findall(r'(\d{4}\-\d{2}\-\d{2})', response.url)

        for horse_tbody in response.xpath("//tbody[contains(concat('',@id,''), 'sc_')]"):

            horse_name = horse_tbody.xpath(
                ".//a[following-sibling::div[@class='horseShortInfo']]//text()").extract()

            horse_number = horse_tbody.xpath(".//td[@class='t']/strong/text()").extract()
            horse_barrier = horse_tbody.xpath(".//td[@class='t']/sup/text()").extract()
            comment = horse_tbody.xpath(".//td[@class='cardItemInfo']/p[@class='diomed']/text()").extract()
            dayssincelast_run = horse_tbody.xpath(
                ".//div[@class='horseShortInfo']/span[preceding::ul[@class='cardControls']]/text()").extract()
            horse_rpTS = horse_tbody.xpath(".//tr[contains(@class,'cr')]/td[7]/text()").extract()
            horse_rpRPR = horse_tbody.xpath(".//tr[contains(@class,'cr')]/td[8]/text()").extract()
            horse_rpOR = horse_tbody.xpath(".//tr[contains(@class,'cr')]/td[5]/div[2]/text()").extract()

            # bestodds = horse_tbody.xpath(".//td[b/following-sibling::a]/text()[last()]").extract()

            item_loader = RacedayItemLoader(item=HorseItem(response.meta['item']), response=response)
            item_loader.add_value('racename', race_name)
            item_loader.add_value('racecourse', race_course)
            item_loader.add_value('raceclass', race_class)
            item_loader.add_value('racepm', race_pm)
            item_loader.add_value('racedistance', race_distance)
            item_loader.add_value('racegoing', race_going)
            item_loader.add_value('racetime', race_time)
            item_loader.add_value('racedate', race_date)
            item_loader.add_value('horsename', horse_name)
            item_loader.add_value('comment', comment)
            item_loader.add_value('timestamp', datetime.now())
            item_loader.add_value('horsenumber', horse_number)
            item_loader.add_value('barrier', horse_barrier)
            item_loader.add_value('dayssincelastrun', dayssincelast_run)
            # item_loader.add_xpath('todaysWgt_dec', ".//tr[contains(@class,'cr')]/td[5]/div[1]/text()")
            # item_loader.add_xpath('todaysWgt', ".//tr[contains(@class,'cr')]/td[5]/div[1]/text()")
            # item_loader.add_xpath('rpRPR', ".//tr[contains(@class,'cr')]/td[8]/text()")
            # item_loader.add_xpath('rpOR', ".//tr[contains(@class,'cr')]/td[5]/div[2]/text()")
            item_loader.add_value('rpTS', horse_rpTS)
            item_loader.add_value('rpRPR', horse_rpRPR)
            item_loader.add_value('rpOR', horse_rpOR)
            # item_loader.add_value('bestodds', bestodds)

            horse_card_href = horse_tbody.xpath(".//a[following-sibling::div[@class='horseShortInfo']]/@href").extract()

            if horse_card_href:
                yield Request(
                    horse_card_href[0],
                    meta={
                        'item': item_loader.load_item()
                    },
                    callback=self.parse_horse_card
                )
            else:
                yield item_loader.load_item()

    def parse_horse_card(self, response):

        sire_href = response.xpath("//ul[@id='detailedInfo']/li[2]/b[1]/a/@href").extract()

        # get stallion
        item_loader = RacedayItemLoader(item=HorseItem(response.meta['item']), response=response)
        item_loader.add_xpath('hage', "//ul[@id='detailedInfo']/li[1]/b/text()", re=r"([\d]+)-y-o.*")
        for index, wgt in enumerate(response.xpath("//div[@id='horse_form']//tr/td[4]//text()").extract()):
            # for index, wgt in enumerate(response.xpath("//div[@id='horse_form']//tr"):
            if index < 5:
                item_loader.add_value('WGT{}'.format(index + 1), wgt)
            else:
                break
        for index, cl in enumerate(
                response.xpath("//div[@id='horse_form']//tr//td[3]/b/following-sibling::text()").extract()):
            # for index, wgt in enumerate(response.xpath("//div[@id='horse_form']//tr"):
            if index < 5:
                item_loader.add_value('ClassL{}'.format(index + 1), cl.strip())
            else:
                break
        for index, cm in enumerate(response.xpath("//div[@id='horse_form']//tr//td[5]/a/@title").extract()):
            # for index, wgt in enumerate(response.xpath("//div[@id='horse_form']//tr"):
            if index < 5:
                item_loader.add_value('L{}comment'.format(index + 1), cm.strip())
            else:
                break

        cleanr = re.compile('<.*?>')
        for index, outcome in enumerate(response.xpath("//div[@id='horse_form']//tr//td[5]").extract()):
            # for index, wgt in enumerate(response.xpath("//div[@id='horse_form']//tr"):
            if index < 5:
                item_loader.add_value('L{}raceoutcome'.format(index + 1), re.sub(cleanr, '', outcome.strip()))
            else:
                break

        if sire_href:
            yield Request(
                sire_href[0],
                meta={
                    'item': item_loader.load_item()
                },
                callback=self.parse_sire,
                dont_filter=True
            )
        else:
            yield item_loader.load_item()

    def parse_sire(self, response):
        main_pedigree_url = "http://www.pedigreequery.com/"

        horsename = response.meta['item']['horsename']
        item_loader = RacedayItemLoader(item=HorseItem(response.meta['item']), response=response)
        item_loader.add_xpath('sirecomment', ".//tr[2]/td/ul/li[4]/strong/text()")

        if horsename:
            pedigree_href = horsename[0].replace(" ", "+")
            ped_href = urlparse.urljoin(main_pedigree_url, pedigree_href)
            yield Request(
                ped_href,
                meta={
                    'item': item_loader.load_item()
                },
                callback=self.parse_pefquery,
                dont_filter=True,
            )
        else:
            yield item_loader.load_item()

    def parse_pefquery(self, response):

        item_loader = RacedayItemLoader(item=HorseItem(response.meta['item']), response=response)
        # [type], [birth year] DP = [dosage profile] (tot points) DI = [dosage index] CD = [center of distribution]
        item_loader.add_xpath('pedstats', "//a[@href='javascript:nothing();']/following-sibling::text()")
        item_loader.add_xpath('DI', "//a[@href='javascript:nothing();']/following-sibling::text()")
        item_loader.add_xpath('CD', "//a[@href='javascript:nothing();']/following-sibling::text()")

        # item_loader.add_xpath('sirename', "//table[@class='pedigreetable']/tr/td[@class='m'][1]/a/text()")
        item_loader.add_xpath('pedigreecomment', "//div[@id='subjectinfo']/table/td[@class='n']")
        return item_loader.load_item()