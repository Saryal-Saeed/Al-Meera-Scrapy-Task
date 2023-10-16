import scrapy
import json


class ItemsscrapeSpider(scrapy.Spider):
    name = "ItemsScrape"
    allowed_domains = ["almeera.online"]
    start_urls = ["https://almeera.online/"]
    base_url= "https://almeera.online/"

    

    def parse(self, response):
        category_URL=[]
        category = response.css("#content .clearfix li")
        for info in category:
            category_title= info.css(".subcategory-name::text").extract()
            category_image=info.css(".subcategory-icon img::attr(src)").get()
            info.urljoin(category_image)
            category_link=response.xpath("//*[@id='content']/div/div/div[3]/div/ul/li/a/@href").get()
            category_URL.append(category_link)

        for links in category_URL:
            yield response.follow(links, self.Subcategories)
        

    def Subcategories(self, response):
        subcategory_list=[]
        subcategories_title=response.css("#content .clearfix li")
        for info in subcategories_title:
            sub_title=response.css(".subcategory-name::text").extract()
            sub_image=response.css(".subcategory-icon img::attr(src)").get()
            sub_urls=response.xpath("//*[@id='content']/div/div/div[3]/div/ul/li/a/@href").get()
        subcategory_list.append(sub_urls)

        for links in subcategory_list:
            yield response.follow(links, self.products_URl)

    def products_URL(self, response):
        
        All_products=response.css("#content .product")
        for item_links in All_products:
            Prodcut_links=item_links.css("#content .url").get()
            product_title=item_links.css("#content .product-name::text").extract()
            product_image=item_links.css("#content .photo::attr(src)").get()
            item_links.urljoin(product_image)
            product_price=item_links.xpath("//span[@class='price product-price']/text()").get()
            
            
        next_page = response.css('.next-page').get()
        if next_page is not None:
            yield response.follow(next_page, self.products_URL)

            
        
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
            item_barcode = ""  # You can add logic to extract the item barcode
            product_data = {
                "ItemTitle": item_title,
                "ItemImageURL": item_image_url,
                "ItemPrice": item_price,
                "ItemBarcode": item_barcode
            }
            subcategory_data["Products"].append(product_data)
        category_data["Subcategories"].append(subcategory_data)

        yield category_data

        next_page = response.css('.next-page a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse_products)

      
