import scrapy
import json


class ItemsscrapeSpider(scrapy.Spider):
    name = "ItemsScrape"
    allowed_domains = ["almeera.online"]
    start_urls = ["https://almeera.online/"]
    base_url = "https://almeera.online/"

    data = []

    def parse(self, response):
        category_list = response.css("#content .clearfix li")
        for category in category_list:
            category_title = category.css(".subcategory-name::text").get()
            category_image = self.base_url + category.css(".subcategory-icon img::attr(src)").get()
            category_data = {
                "CategoryTitle": category_title,
                "CategoryImageURL": category_image,
                "Subcategories": []
            }
            category_link = category.css("a::attr(href)").get()
            yield response.follow(category_link, self.parse_subcategories, meta={'category_data': category_data})

    def parse_subcategories(self, response):
        category_data = response.meta['category_data']
        subcategory_list = response.css("#content .clearfix li")
        for subcategory in subcategory_list:
            subcategory_title = subcategory.css(".subcategory-name::text").get()
            products = []
            subcategory_data = {
                "SubcategoryTitle": subcategory_title,
                "Products": products
            }
            subcategory_link = subcategory.css("a::attr(href)").get()
            yield response.follow(subcategory_link, self.parse_products, meta={'category_data': category_data, 'subcategory_data': subcategory_data})

    def parse_products(self, response):
        category_data = response.meta['category_data']
        subcategory_data = response.meta['subcategory_data']
        products_list = response.css("#content .product")
        for product in products_list:
            item_title = product.css(".product-name::text").get()
            item_image_url = self.base_url + product.css(".photo::attr(src)").get()
            item_price = product.css("span.price.product-price::text").get()
         
            product_data = {
                "ItemTitle": item_title,
                "ItemImageURL": item_image_url,
                "ItemPrice": item_price,
               
            }
            subcategory_data["Products"].append(product_data)
        category_data["Subcategories"].append(subcategory_data)

        yield category_data

        next_page = response.css('.next-page a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse_products)

      
