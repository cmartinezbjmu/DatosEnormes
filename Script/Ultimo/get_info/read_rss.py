# -*- coding: utf-8 -*-

import feedparser
from pymongo import MongoClient, errors
from bs4 import BeautifulSoup
import requests

feeds_rss = ['https://www.eltiempo.com/rss/colombia.xml',
'https://www.eltiempo.com/rss/opinion.xml',
'https://www.eltiempo.com/rss/colombia_barranquilla.xml',
'https://www.eltiempo.com/rss/colombia_medellin.xml',
'https://www.eltiempo.com/rss/colombia_cali.xml',
'https://www.eltiempo.com/rss/colombia_otras-ciudades.xml',
'https://www.eltiempo.com/rss/bogota.xml',
'https://www.eltiempo.com/rss/politica.xml',
'https://www.eltiempo.com/rss/politica_gobierno.xml',
'https://www.eltiempo.com/rss/politica_congreso.xml',
'https://www.eltiempo.com/rss/economia.xml',
'https://www.eltiempo.com/rss/economia_sectores.xml',
'https://www.eltiempo.com/rss/economia_sector-financiero.xml',
'https://www.eltiempo.com/rss/cultura.xml',
'https://www.eltiempo.com/rss/tecnosfera_novedades-tecnologia.xml',
'https://www.eltiempo.com/rss/vida.xml',
'https://www.eltiempo.com/rss/vida_educacion.xml',
'https://www.eltiempo.com/rss/vida_ciencia.xml',
'https://www.portafolio.co/rss/',
'http://portafolio.co/rss/economia',
'http://portafolio.co/rss/economia/gobierno',
'http://portafolio.co/rss/economia/empleo',
'http://portafolio.co/rss/negocios/empresas',
'http://portafolio.co/rss/tendencias',
'http://portafolio.co/rss/tendencias/entretenimiento',
'http://www.bbc.co.uk/mundo/temas/america_latina/index.xml',
'http://www.bbc.co.uk/mundo/temas/ciencia/index.xml',
'http://www.bbc.co.uk/mundo/temas/salud/index.xml',
'http://www.bbc.co.uk/mundo/temas/economia/index.xml',
'https://www.bbc.com/mundo/temas/america_latina/index.xml#sa-link_location=story-body&intlink_from_url=https%3A%2F%2Fwww.bbc.com%2Fmundo%2Finstitucional%2F2011%2F03%2F000000_rss_gel&intlink_ts=1587832474716-sa',
'https://www.cancilleria.gov.co/rss.xml',
'http://feeds.feedburner.com/eluniversal/ctg_amb',
'http://feeds.feedburner.com/eluniversal/ctg_ciencia',
'https://www.contratos.gov.co/Archivos/RSSFolder/RSSFiles/rssFeed-42000000.xml',
'https://www.contratos.gov.co/Archivos/RSSFolder/RSSFiles/rssFeed-76000000.xml',
'https://www.contratos.gov.co/Archivos/RSSFolder/RSSFiles/rssFeed-51000000.xml',
'https://www.contratos.gov.co/Archivos/RSSFolder/RSSFiles/rssFeed-85000000.xml',
'https://www.rcnradio.com/rss.xml',
'https://www.integracionsocial.gov.co/index.php/secretaria-distrital-de-integracion-social-rss?format=feed&type=rss',
'https://id.presidencia.gov.co/_layouts/15/feed.aspx?xsl=1&web=%2F&page=bbc76620-7657-48b2-aeb0-83511535bb52&wp=043782e4-c9ed-46e5-8715-1688effcaedf&pageurl=%2FPaginas%2FRSS%2Easpx',
'https://www.elcolombiano.com/rss/Colombia.xml',
'https://www.shd.gov.co/shd/rss.xml',
'https://colombiareports.com/feed/',
'https://www.colombia.com/rss/']

feeds_rss = [#'https://www.integracionsocial.gov.co/index.php/secretaria-distrital-de-integracion-social-rss?format=feed&type=rss',
#'https://id.presidencia.gov.co/_layouts/15/feed.aspx?xsl=1&web=%2F&page=bbc76620-7657-48b2-aeb0-83511535bb52&wp=043782e4-c9ed-46e5-8715-1688effcaedf&pageurl=%2FPaginas%2FRSS%2Easpx',
'https://www.elcolombiano.com/rss/Colombia.xml',
'https://www.shd.gov.co/shd/rss.xml',
'https://colombiareports.com/feed/',
'https://www.colombia.com/rss/']

def obtener_texto_eltiempo(link):
    response = requests.get(link)
    souplist = BeautifulSoup(response.text, "html.parser")
    #print(souplist)
    texto = ''
    for parrafo in souplist.find_all('p',{"class":"contenido"}):
        texto = texto + parrafo.text
    
    return texto

def obtener_texto_portafolio(link):
    response = requests.get(link)
    souplist = BeautifulSoup(response.text, "html.parser")
    texto = ''
    for parrafo in souplist.find_all('p',{"class":"parrafo first-parrafo"}):
        texto = texto + parrafo.text
    for parrafo in souplist.find_all('p',{"class":"parrafo"}):
        texto = texto + parrafo.text
    return texto

def obtener_texto_bbc(link):
    response = requests.get(link)
    souplist = BeautifulSoup(response.text, "html.parser")
    #print(souplist)
    texto = ''
    for parrafo in souplist.find_all('p'):
        texto = texto + parrafo.text + '\n'
    
    return texto

def obtener_texto_cancilleria(link):    
    souplist = BeautifulSoup(link, "html.parser")
    #print(souplist)
    texto = ''
    for parrafo in souplist.find_all('p'):
        texto = texto + parrafo.text + '\n'
    
    return texto

def obtener_texto_universal(link):
    response = requests.get(link)
    souplist = BeautifulSoup(response.text, "html.parser")
    #print(souplist)
    texto = ''
    for parrafo in souplist.find_all('p'):
        texto = texto + parrafo.text + '\n'
    
    return texto

def obtener_texto_contratos(link):
    texto = BeautifulSoup(link, "html.parser").text    
    #print(souplist)   
    
    return texto

def obtener_texto_rcn(link):
    texto = BeautifulSoup(link, "html.parser").text
    #print(souplist)
    
    return texto

def obtener_texto_sec_integracion(link):
    response = requests.get(link)
    souplist = BeautifulSoup(response.text, "html.parser")
    #print(souplist)
    texto = ''
    for parrafo in souplist.find('div', {"id":"quijote"}).text:
        texto = texto + parrafo
    
    return texto

def obtener_texto_presidencia(link):
    response = requests.get(link)
    souplist = BeautifulSoup(response.text, "html.parser")
    #print(souplist)
    texto = ''
    try:
        for parrafo in souplist.find('div', {"data-name":"Campo de página: Contenido de la página"}).text:
            texto = texto + parrafo
    except: pass
    
    return texto

def obtener_texto_colombia(link):
    response = requests.get(link)
    souplist = BeautifulSoup(response.text, "html.parser")
    #print(souplist)
    texto = ''
    try:
        for parrafo in souplist.find('div', {"class":"notice-body"}).text:
            texto = texto + parrafo

        return texto
    except:
        pass
    

for fuente in feeds_rss:
    try:
        client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/", retryWrites=False, serverSelectionTimeoutMS=10, connectTimeoutMS=20000)
        client.server_info() # force connection on a request as the
                            # connect=True parameter of MongoClient seems
                            # to be useless here
        db = client.Grupo03
        collection = db.RSS_feed
    
        feed = feedparser.parse(fuente)
        for item in feed['items']:
            try:
                if 'eltiempo' in item['link']:
                    item['noticia'] = obtener_texto_eltiempo(item['link'])#                
                if 'portafolio' in item['link']:
                    item['noticia'] = obtener_texto_portafolio(item['link'])
                if 'bbc' in item['link']:
                    item['noticia'] = obtener_texto_bbc(item['link'])
                if 'cancilleria' in item['link']:
                    item['noticia'] = obtener_texto_cancilleria(item['description'])
                if 'eluniversal' in item['link']:
                    item['noticia'] = obtener_texto_universal(item['link'])
                if 'contratos' in item['link']:
                    item['noticia'] = obtener_texto_contratos(item['description'])
                if 'rcn' in item['link']:
                    item['noticia'] = obtener_texto_rcn(item['description'])
                if 'integracionsocial' in item['link']:
                    item['noticia'] = obtener_texto_sec_integracion(item['link'])
                if 'presidencia' in item['link']:
                    item['noticia'] = obtener_texto_presidencia(item['link'])
                if 'colombia.com' in item['link']:
                    print(item['link'])
                    item['noticia'] = obtener_texto_colombia(item['link'])

                
                collection.insert_one(item)
            except KeyError:
                continue
        try:
            print('Terminó fuente: ' + feed['feed']['title'])
        except KeyError:
            continue
   
    except errors.ServerSelectionTimeoutError as err:
        # do whatever you need
        print(err)


#feed = feedparser.parse('https://www.rcnradio.com/rss.xml')
#for item in feed['items']:
#    print(obtener_texto_contratos(item['description']))

#print(obtener_texto_presidencia('https://www.colombia.com/horoscopo/diario/horoscopo-19-mayo-josie-diez-canseco-270543'))
