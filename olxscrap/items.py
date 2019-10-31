# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OlxscrapItem(scrapy.Item):
    #list of dictionary
    Url                     = scrapy.Field()
    Merek                   = scrapy.Field()
    Varian                  = scrapy.Field()
    Model                   = scrapy.Field()
    Tahun                   = scrapy.Field()
    TanggalJual             = scrapy.Field()
    JarakTempuh             = scrapy.Field()
    BahanBakar              = scrapy.Field()
    Warna                   = scrapy.Field()
    Transmisi               = scrapy.Field()
    Lokasi                  = scrapy.Field()
    NamaPenjual             = scrapy.Field()
    TanggalAnggota          = scrapy.Field()
    NamaBursaMobil          = scrapy.Field()
    TipeBodi                = scrapy.Field()
    SistemPenggerak         = scrapy.Field()
    KapasitasMesin          = scrapy.Field()
    FiturTambahan           = scrapy.Field()
    TipePenjual             = scrapy.Field()
    dihighlight             = scrapy.Field()
    Harga                   = scrapy.Field()