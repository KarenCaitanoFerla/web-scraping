import scrapy
import warnings
warnings.filterwarnings("ignore", category=scrapy.exceptions.ScrapyDeprecationWarning)

class Sp1Spider(scrapy.Spider):
    name = 'scraper'
    start_urls = ['https://www.amocanecas.com.br/presentes-canecas-personalizadas-datas-comemorativas'] #site de canecas

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
    
    def start_requests(self):
        for url in self.start_urls:
            url = 'https://www.amocanecas.com.br/presentes-canecas-personalizadas-datas-comemorativas'
            yield scrapy.Request(url=url, callback = self.parse, headers = self.headers)

    def parse(self,response):

        anuncios = response.xpath('//div[@class="acoes-produto-responsiva visible-phone"]/a')
        for a in anuncios:
            url = a.xpath('./@href').extract_first()
            yield scrapy.Request(url=url, callback = self.parse_detail,  dont_filter=True, headers = self.headers, method = 'GET')

    def parse_detail(self, response):

        titulo = response.xpath('//h1[@class="nome-produto titulo cor-secundaria"]/text()').extract_first()
        valor = response.xpath('//div[@class="row-fluid"][contains(.,"Cód")]//span[@class="desconto-a-vista"]/strong/text()').extract_first()
        descricao = response.xpath('//div[@class="tab-pane active"]/p//text()').getall()
        desc = ''.join(descricao)
        fotos = response.xpath('//div[@class="produto-thumbs"]//img/@src').getall()
        url = response.url

        items = {
            'titulo': titulo,
            'valor': valor,
            'descricao': desc,
            'fotos': fotos,
            'url_anuncio': url
        }

        yield items



