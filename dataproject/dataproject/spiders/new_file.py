import scrapy
import pandas
import FormRequest


class FacebookSpider(scrapy.Spider):
    name = "fb_text"

    def __init__(self, email='', password='', **kwargs):
        super(FacebookSpider, self).__init__(**kwargs)

        self.dict = {}
        self.Name = []
        self.Text = []
        self.Time = []

        if not email or not password:
            raise ValueError("You need to provide valid email and password!")
        else:
            self.email = email
            self.password = password

        self.start_urls = ['https://mbasic.facebook.com']

    def parse(self, response):
        return FormRequest.from_response(
            response,
            formxpath='//form[contains(@action, "login")]',
            formdata={'email': self.email, 'pass': self.password},
            callback=self.parse_home
        )

    def parse_home(self, response):
        href = 'https://mbasic.facebook.com/messages/?ref_component=mbasic_home_header&ref_page=%2Fwap%2Fprofile_timeline.php&refid=17'
        return scrapy.Request(url=href, callback=self.parse_page, )

    def parse_page(self, response):
        res = response.body
        peoples = Selector(text=res).xpath('//h3/a/text()').extract()
        people_link = Selector(text=res).xpath('//h3/a/@href').extract()
        print('Choose the conversation')
        print(peoples, people_link)
        for i in range(len(peoples)):
            print(i, peoples[i])
        convo = int(input())

        yield scrapy.Request(url='https://mbasic.facebook.com' + people_link[convo], callback=self.parse_convo)
