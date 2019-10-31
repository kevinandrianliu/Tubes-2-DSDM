import scrapy
from bs4 import BeautifulSoup
import re
from olxscrap.items import OlxscrapItem


class OlxscrapSpider(scrapy.Spider):
    name = 'OlxscrapSpider'
    link = []
    for i in range(60):
        link.append('https://www.olx.co.id/mobil-bekas_c198')
    start_urls = link

    def __init__(self):
        self.declare_css()

        #All the XPaths the spider needs to know go here
    def declare_css(self):
        self.getAllItemscss = "li[class=EIR5N] a::attr(href)"
        self.Merekcss  = "span[data-aut-id=value_make]::text"
        self.Variancss = "span[data-aut-id=value_m_tipe_variant]::text"
        self.Modelcss = "span[data-aut-id=value_m_tipe]::text"
        self.Tahuncss = "span[data-aut-id=value_m_year]::text"
        self.TanggalJualcss = "span[data-aut-id=value_make]::text"
        self.JarakTempuhcss = "span[data-aut-id=value_mileage]::text"
        self.BahanBakarcss = "span[data-aut-id=value_m_fuel]::text"
        self.Warnacss = "span[data-aut-id=value_m_color]::text"
        self.Transmisicss = "span[data-aut-id=value_m_transmission]::text"
        self.Lokasicss = "span[class=_2FRXm]::text"
        self.NamaPenjualcss = "div[class=_3oOe9]::text"
        self.TanggalAnggotacss = "div[data-aut-id=memberSince] span span::text"
        self.NamaBursaMobilcss = "span[data-aut-id=value_m_exchange]::text"
        self.TipeBodicss = "span[data-aut-id=value_m_body]::text"
        self.SistemPenggerakcss = "span[data-aut-id=value_m_drivetrain]::text"
        self.KapasitasMesincss = "span[data-aut-id=value_m_engine_capacity]::text"
        self.FiturTambahancss = "span[class=_30Ijq]::text"
        self.TipePenjualcss = "span[data-aut-id=value_m_seller_type]::text"
        self.dihighlightcss = "label[class=jW_R5] span::text"
        self.Hargacss = "._2xKfz::text"



    def parse(self,response):
        for href in response.css(self.getAllItemscss):
            print(href)
            url = response.urljoin(href.extract())
            yield scrapy.Request(url,callback=self.parse_main_item, dont_filter=True)

    
    def parse_main_item(self,response):
        item = OlxscrapItem()

        Merek = response.css(self.Merekcss).extract()
        # Merek = self.cleanText(self.parseText(Merek))

        Varian = response.css(self.Variancss).extract()
        # Varian = self.cleanText(self.parseText(Varian))

        Model = response.css(self.Modelcss).extract()
        # Model = self.cleanText(self.parseText(Model))

        Tahun = response.css(self.Tahuncss).extract()
        # Tahun = self.cleanText(self.parseText(Tahun))

        TanggalJual = response.css(self.TanggalJualcss).extract()
        # TanggalJual = self.cleanText(self.parseText(TanggalJual))

        JarakTempuh = response.css(self.JarakTempuhcss).extract()
        # JarakTempuh = self.cleanText(self.parseText(JarakTempuh))

        BahanBakar = response.css(self.BahanBakarcss).extract()
        # BahanBakar = self.cleanText(self.parseText(BahanBakar))

        Warna = response.css(self.Warnacss).extract()
        # Warna = self.cleanText(self.parseText(Warna))

        Transmisi = response.css(self.Transmisicss).extract()
        # Transmisi = self.cleanText(self.parseText(Transmisi))

        Lokasi = response.css(self.Lokasicss).extract()

        NamaPenjual = response.css(self.NamaPenjualcss).extract()

        TanggalAnggota = response.css(self.TanggalAnggotacss).extract()

        NamaBursaMobil = response.css(self.NamaBursaMobilcss).extract()

        TipeBodi = response.css(self.TipeBodicss).extract()
        # TipeBodi = self.cleanText(self.parseText(TipeBodi))

        SistemPenggerak = response.css(self.SistemPenggerakcss).extract()
        # SistemPenggerak = self.cleanText(self.parseText(SistemPenggerak))

        KapasitasMesin = response.css(self.KapasitasMesincss).extract()
        # KapasitasMesin = self.cleanText(self.parseText(KapasitasMesin))

        FiturTambahan = response.css(self.FiturTambahancss).extract()
        # FiturTambahan = self.cleanText(self.parseText(FiturTambahan))
        
        TipePenjual = response.css(self.TipePenjualcss).extract()
        # TipePenjual = self.cleanText(self.parseText(TipePenjual))

        dihighlight = response.css(self.dihighlightcss).extract()
        # dihighlight = self.cleanText(self.parseText(dihighlight))

        Harga = response.css(self.Hargacss).extract()
        # Harga = self.cleanText(self.parseText(Harga))


        #Put each element into item attribute.
        item['Url']             = response.url
        item['Merek']           = Merek
        item['Varian']          = Varian
        item['Model']           = Model
        item['Tahun']           = Tahun
        item['TanggalJual']     = TanggalJual
        item['JarakTempuh']     = JarakTempuh
        item['BahanBakar']      = BahanBakar
        item['Warna']           = Warna
        item['Transmisi']       = Transmisi
        item['Lokasi']          = Lokasi
        item['NamaPenjual']     = NamaPenjual
        item['TanggalAnggota']  = TanggalAnggota
        item['NamaBursaMobil']  = NamaBursaMobil
        item['TipeBodi']        = TipeBodi
        item['SistemPenggerak'] = SistemPenggerak
        item['KapasitasMesin']  = KapasitasMesin
        item['FiturTambahan']   = FiturTambahan
        item['TipePenjual']     = TipePenjual
        item['dihighlight']     = dihighlight
        item['Harga']           = Harga
        return item
 
    #Methods to clean and format text to make it easier to work with later
    def listToStr(self,MyList):
        dumm = ""
        MyList = [i.encode('utf-8') for i in MyList]
        for i in MyList:dumm = "{0}{1}".format(dumm,i)
        return dumm
 
    def parseText(self, str):
        soup = BeautifulSoup(str, 'html.parser')
        return re.sub(" +|\n|\r|\t|\0|\x0b|\xa0",' ',soup.get_text()).strip()
 
    def cleanText(self,text):
        soup = BeautifulSoup(text,'html.parser')
        text = soup.get_text()
        text = re.sub("( +|\n|\r|\t|\0|\x0b|\xa0|\xbb|\xab)+",' ',text).strip()
        return text
