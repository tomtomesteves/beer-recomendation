import scrapy


class TesteSpider(scrapy.Spider):
    name = "beers"

    def start_requests(self):
        # Coleta a url de cada estado
        urls = ["https://www.brejas.com.br/cerveja/cerveja-por-cervejaria"]
        # urls = response.css(
        #     '.jr-fields-module').css('li').css('a::attr(href)').extract()

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_brewerys)

    def parse_brewerys(self, response, **kwargs):
        yield from response.follow_all(css='.jr-fields-module a', callback=self.parse_beers)

    def parse_beers(self, response):
        yield from response.follow_all(css='.jrListingTitle a', callback=self.parse_beer_info)

    def parse_beer_info(self, response):
        def extract_rating(value):
            return value.split("\xa0")[0]

        def extract_number_ratings(value):
            return value.split("\xa0")[2].replace("(", "").replace(")", "")

        if response.css(".jrTableGrid.jrRatingTable").css(".jrCol.jrRatingValue::text").extract():
            yield {
                "beer_name":  response.css(".contentheading span::text").get(),
                "brewerys": response.css(".jrFieldRow.jrCervejaria").css(".jrFieldValue span::text").get(),
                "beer_type": response.css(".jrFieldRow.jrEstilo").css(".jrFieldValue a::text").get(),
                "alcohol_volume": response.css(".jrFieldRow.jrAlcool").css(".jrFieldValue::text").get(),
                "ingredientes": response.css(".jrFieldRow.jrIngredientes").css(".jrFieldValue::text").get(),
                "is_active": response.css(".jrFieldRow.jrAtiva").css(".jrFieldValue a::text").get(),
                "is_sazonal": response.css(".jrFieldRow.jrSazonal").css(".jrFieldValue a::text").get(),
                "rec_temperature": response.css(".jrFieldRow.jrTemperatura").css(".jrFieldValue a::text").get(),
                "rec_glass": response.css(".jrFieldRow.jrCopo").css(".jrFieldValue a::text").get(),
                "description": response.css(".jrListingFulltext::text").get(),
                "average_rating": response.css(".jrTableGrid.jrRatingTable").css(".jrCol.jrRatingValue::text").extract()[0],
                "smelling_rating": extract_rating(response.css(".jrTableGrid.jrRatingTable").css(".jrCol.jrRatingValue::text").extract()[1]),
                "Appearance_rating": extract_rating(response.css(".jrTableGrid.jrRatingTable").css(".jrCol.jrRatingValue::text").extract()[2]),
                "flavor_rating": extract_rating(response.css(".jrTableGrid.jrRatingTable").css(".jrCol.jrRatingValue::text").extract()[3]),
                "Sensation_rating": extract_rating(response.css(".jrTableGrid.jrRatingTable").css(".jrCol.jrRatingValue::text").extract()[4]),
                "ensemble_rating": extract_rating(response.css(".jrTableGrid.jrRatingTable").css(".jrCol.jrRatingValue::text").extract()[5]),
                "number_ratings": extract_number_ratings(response.css(".jrTableGrid.jrRatingTable").css(".jrCol.jrRatingValue::text").extract()[5]),
                "country": response.url.split("/")[-2]
            }
        else:
            yield {
                "beer_name":  response.css(".contentheading span::text").get(),
                "brewerys": response.css(".jrFieldRow.jrCervejaria").css(".jrFieldValue span::text").get(),
                "beer_type": response.css(".jrFieldRow.jrEstilo").css(".jrFieldValue a::text").get(),
                "alcohol_volume": response.css(".jrFieldRow.jrAlcool").css(".jrFieldValue::text").get(),
                "ingredientes": response.css(".jrFieldRow.jrIngredientes").css(".jrFieldValue::text").get(),
                "is_active": response.css(".jrFieldRow.jrAtiva").css(".jrFieldValue a::text").get(),
                "is_sazonal": response.css(".jrFieldRow.jrSazonal").css(".jrFieldValue a::text").get(),
                "rec_temperature": response.css(".jrFieldRow.jrTemperatura").css(".jrFieldValue a::text").get(),
                "rec_glass": response.css(".jrFieldRow.jrCopo").css(".jrFieldValue a::text").get(),
                "description": response.css(".jrListingFulltext::text").get(),
                "average_rating": None,
                "smelling_rating": None,
                "Appearance_rating": None,
                "flavor_rating": None,
                "Sensation_rating": None,
                "ensemble_rating": None,
                "number_ratings": 0,
                "country": response.url.split("/")[-2]
            }
