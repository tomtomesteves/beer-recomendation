import scrapy


class TesteSpider(scrapy.Spider):
    name = "reviews"

    def start_requests(self):
        # Coleta a url de cada cerveja brasileira
        urls = ["https://www.brejas.com.br/cerveja/brasil"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_beers)

    def parse_beers(self, response):
        yield from response.follow_all(css='.jrListingTitle a', callback=self.parse_reviews)
        yield from response.follow_all(css="""#jr-pagenav-ajax > div.jr-pagenav.jrTableGrid.jrPagination.jrPaginationTop
                                            > div.jrCol4.jrPagenavPages > a.jr-pagenav-next.jrButton.jrSmall""",
                                       callback=self.parse_beers)

    def go_to_all_review(self, response):
        yield from response.follow_all(css='.#userReviews a', callback=self.parse_reviews)

    def parse_reviews(self, response):
        def extract_rating(value):
            return value.split("\xa0")[0]

        div_num = 5
        if not response.xpath('//*[@id="userReviews"]/div[{}]/div/div'.format(div_num)):
            div_num = 3

        for child in response.xpath('//*[@id="userReviews"]/div[{}]/div/div'.format(div_num)):
            reviews = child.css(".jrRatingValue::text").getall()
            # self.logger.info(reviews)
            yield {
                "user_name": child.css(".jrUserInfoText span::text").get(),
                "beer_name": response.css(".contentheading span a::text").get(),
                "review_commentary": response.css("div.description.jrReviewComment div::text").get(),
                "overall": extract_rating(reviews[0]),
                "aroma": extract_rating(reviews[1]),
                "appearance": extract_rating(reviews[2]),
                "flavor": extract_rating(reviews[3]),
                "sensation": extract_rating(reviews[4]),
                "ensemble": extract_rating(reviews[5])
            }
