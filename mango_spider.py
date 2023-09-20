import json
import scrapy


class MangoSpider(scrapy.Spider):
    name = "mango_spider"
    start_urls = [
        "https://shop.mango.com/services/productlist/products/BG-en/"
        "he/sections_he.promocionado_nueva_temporada_he/?pageNum=1&rows"
        "PerPage=1000&columnsPerRow=4&family=115&idSubSection=camisetas_he",
    ]

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        all_products = []
        target_garment_id = 'g4709592307'
        for group in json_response.get('groups', []):
            for garment_id, garment_info in group.get('garments', {}).items():
                product = {
                    'id': garment_id,
                    'name': garment_info.get('name', ''),
                    'description': garment_info.get('shortDescription', ''),
                    'stock': garment_info.get('stock', 0),
                    'genre': garment_info.get('genre', ''),
                    'colors': garment_info.get('colors', []),
                    'salePrice': garment_info.get('price', {}).get('salePrice', ''),
                }

                name = product['description']
                sale_price = garment_info.get('price', {}).get('salePrice', '')
                price_text = sale_price.replace("лв.", "").replace(",", ".")
                finally_price = float(price_text)
                colors = product['colors'][0]['label']
                sizes_with_stock = [
                    size['label']
                    for size in product['colors'][0]['sizes']
                    if size['stock'] != 0
                ]
                if garment_id == target_garment_id:
                    data = {
                        "name": name,
                        "price": finally_price,
                        "colour": colors,
                        "size": sizes_with_stock,
                    }
                    all_products.append(data)

            self.save_data_to_json(all_products, 'product_id_47095923.json')

    def save_data_to_json(self, data, filename):
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
