from urllib import parse
from time import sleep
import re
import json
import scrapy
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from ArticleCnblogsSpider.items import ArticleItemLoader
from ArticleCnblogsSpider.items import ArticlecnblogsspiderItem
from ArticleCnblogsSpider.utils import common


class CnblogsSpider(scrapy.Spider):
    name = "cnblogs"
    allowed_domains = ["news.cnblogs.com"]
    start_urls = ["https://news.cnblogs.com"]

    def start_requests(self):
        driver = uc.Chrome()
        driver.get('https://account.cnblogs.com/signin')
        user_name = WebDriverWait(driver, 10, 0.2).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="mat-input-0"]')))
        user_name.send_keys('ztraveller@163.com')
        password = WebDriverWait(driver, 10, 0.2).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="mat-input-1"]')))
        password.send_keys('zy19971006')
        login_btn = driver.find_element(By.XPATH, '/html/body/app-root/app-sign-in-layout/div/div/app-sign-in/app-cont'
                                                  'ent-container/div/div/div/form/div/button')
        login_btn.click()
        sleep(2)
        yanzhen = WebDriverWait(driver, 10, 0.2).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="rectTop"]')))
        yanzhen.click()
        sleep(2)
        cookies = driver.get_cookies()
        driver.close()
        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie['name']] = cookie['value']
        for url in self.start_urls:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
                'referer': 'https://news.cnblogs.com/'}
            yield scrapy.Request(url=url, cookies=cookie_dict, headers=headers, dont_filter=True, callback=self.parse)

    def parse(self, response):
        post_nodes = response.xpath('//div[@id="news_list"]//div[@class="news_block"]')[1:2]
        for post_node in post_nodes:
            image_url = post_node.xpath('//div[@class="entry_summary"]/a/img/@src').extract_first("")
            post_url = post_node.xpath('//h2/a/@href').extract_first("")
            if image_url.startswith("//"):
                image_url = f"https:{image_url}"
            yield scrapy.Request(url=parse.urljoin(response.url, post_url), meta={'image_url': image_url},
                                 callback=self.parse_detail)
        # next_url = response.xpath('//a[contains(text(), "Next >")]/@href').extract_first("")
        # yield scrapy.Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        url_id = re.findall('.*?(\d+)', response.url)
        if url_id[0]:
            artice_items_loder = ArticleItemLoader(item=ArticlecnblogsspiderItem(), response=response)
            artice_items_loder.add_xpath('title', '//div[@id="news_title"]/a/text()')
            artice_items_loder.add_xpath('created_date', '//div[@id="news_info"]/span[@class="time"]/text()')
            artice_items_loder.add_value('url', response.url)
            artice_items_loder.add_value('front_image_url', response.meta.get('image_url', ""))
            artice_items_loder.add_xpath('tags', '//div[@class="news_tags"]/a/text()')
            artice_items_loder.add_css('content', "#news_content")
            yield scrapy.Request(url=parse.urljoin(response.url, f"/NewsAjax/GetAjaxNewsInfo?contentId={url_id[0]}"),
                                 meta={"artice_items_loder": artice_items_loder, "url": response.url},
                                 callback=self.parse_news_ajax)

    def parse_news_ajax(self, response):
        res_data = json.loads(response.text)
        artice_items_loder = response.meta.get("artice_items_loder", "")
        artice_items_loder.add_value('praise_num', res_data["DiggCount"])
        artice_items_loder.add_value('comment_nums', res_data["CommentCount"])
        artice_items_loder.add_value('fav_nums', res_data["TotalView"])
        artice_items_loder.add_value('url_object_id', common.get_md5(response.meta.get("url", "")))
        article_items = artice_items_loder.load_item()
        yield article_items
