import scrapy
import undetected_chromedriver as uc


class CnblogSpider(scrapy.Spider):
    name = "cnblog"
    allowed_domains = ["news.cnblogs.com"]
    start_urls = ["https://news.cnblogs.com"]

    def start_requests(self):
        # 从入口可以模拟登录拿到cookie，selenium控制浏览器会被一些网站识别出来，拉钩、知乎
        driver = uc.Chrome()
        driver.get("https://account.cnblogs.com/signin")
        cookies = driver.get_cookies()
        cookie_dict = {}
        for cookie in cookies:
            # 将cookie交给scrapy
            cookie_dict[cookie['name']] = cookie['value']

        for url in self.start_urls:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                              ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
            }
            yield scrapy.Request(url, cookies=cookie_dict, headers=headers, dont_filter=True, callback=self.parse)

    def parse(self, response):
        pass
