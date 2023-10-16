import scrapy
import json


class AlmeeraSpider(scrapy.Spider):
    name = 'almeera'
    allowed_domains = ['almeera.com']
    start_urls = ['https://www.almeera.online/']  
    base_url= "https://www.almeera.online"

    data = []

    def parse(self, response):
        category_title = response.css('your_category_title_selector::text').get()
        category_image_url = response.css('your_category_image_selector::attr(src)').get()

        category_data = {
            "CategoryTitle": category_title,
            "CategoryImageURL": category_image_url,
            "Subcategories": self.parse_subcategories(response)
        }

        self.data.append(category_data)

        next_page = response.css('your_next_page_selector::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

        with open('output.json', 'w') as f:
            json.dump(self.data, f, indent=4)

    def parse_subcategories(self, response):
        subcategories = []
        for subcategory in response.css('your_subcategory_css_selector'):
            subcategory_title = subcategory.css('your_subcategory_title_css_selector::text').get()
            products = self.parse_products(subcategory)

            subcategory_data = {
                "SubcategoryTitle": subcategory_title,
                "Products": products
            }
            subcategories.append(subcategory_data)

        return subcategories

    def parse_products(self, subcategory):
        products = []
        for product in subcategory.css('your_product_css_selector'):
            item_title = product.css('your_item_title_css_selector::text').get()
            item_image_url = product.css('your_item_image_css_selector::attr(src)').get()
            item_price = product.css('your_item_price_css_selector::text').get()
            

            product_data = {
                "ItemTitle": item_title,
                "ItemImageURL": item_image_url,
                "ItemPrice": item_price,
               
            }
            products.append(product_data)

        return products
