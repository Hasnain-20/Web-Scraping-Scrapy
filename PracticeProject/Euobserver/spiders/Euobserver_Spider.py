import scrapy


class EuobserverSpiderSpider(scrapy.Spider):
    name = "Euobserver_Spider"
    allowed_domains = ["euobserver.com"]

    headers = {
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    # 'Referer': 'https://euobserver.com/search?query=',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    }

    def start_requests(self):
        url = "https://euobserver.com/search?query="
        keywords = ['Digital Market Act', 'Digital Services Act', 'GDPR', 'Data Privacy', 'Cybersecurity', 'ePrivacy Regulation', 'Copyright Directive', 'Data Governance Act' , 'The Cybersecurity Act']
        keywords = [i.replace(" ","+") for i in keywords]
        for keyw in keywords:
            yield scrapy.Request(url = url+keyw, callback=self.parse, headers=self.headers)
        
    def parse(self, response):
        articleLinks = response.css('.col-12>h5>a::attr("href")').getall()
        query = response.url.split('=')[1]
        for link in articleLinks:
            yield response.follow(url = link, callback = self.parseArticles, headers=self.headers, meta={'key':query})
        nextPage = response.css('input[name=next]::attr("data-offset")').get()
        if nextPage:
            yield response.follow(f'https://euobserver.com/search?query={query}&sort=date&from=&to=&offset={nextPage}', self.parse, headers=self.headers)

    def parseArticles(self, response):
        article_Title = response.css('h1::text').get()
        article_Url = response.url
        author = response.css('span>a[rel=author]::text').get()
        headline = ' '.join(response.css('.body>p::text').getall())
        email_text = response.css('a[data-icon="o"]::attr("href")').get()
        if email_text:
            email = email_text.split('mailto:')[-1]
        else:
            email = ""
        twitter_text = response.css('a[data-icon="o"]+a::attr("href")').get()
        if twitter_text:
            twitter = twitter_text 
        else:
            twitter = ""
        keyUsed = response.meta.get('key').replace('+',' ').split('&')[0]
        data = {
            "Platform" : "Euobserver", 
            "Article Title" : article_Title, 
            "Article Url" : article_Url,
            "Keyword" : keyUsed, 
            "Authors Name": author,
            "Authros Email" : email, 
            "Authors Twitter" : twitter, 
            "Authors Headline" : headline, 
        }
        yield data
