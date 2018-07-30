"""Uvoz podatkov"""

import requests
import os
import re

url = 'http://store.steampowered.com/search/?category1=998&filter=topsellers&page='

pot = 'spletne_strani'

def nalozi_strani(delni_url, stevilo):
	os.makedirs(pot, exist_ok=True)
	for index in range(1, stevilo + 1):
		stran = requests.get(delni_url + '{}'.format(index))
		with open(os.path.join(pot, 'stran_{}.html'.format(index)),
		'w', encoding='utf-8') as datoteka:
			datoteka.write(stran.text)

#nalozi_strani(url, 5)

iskani_niz = re.compile(
	r'<a href="(?P<url>http://store.steampowered.com/app/.*?)"  data-ds.*?'
	r'<span class="title">(?P<ime>.+?)</span>'
	r'.*?'
	r'row">(?P<datum>\d{1,2} [A-Z][a-z]{2}, (?P<leto>\d{4}))</div>'
	r'.*?'
	r'br&gt;(?P<odstotek>\d{1,2})% of the (?P<stevilo_ocen>(\d|,)*) user'
	r'.*?</span>',
	flags=re.DOTALL
)

def igre_stran(niz, stran, meja_leto=2017, meja_ocene=1000, slovar_iger = {}):
    """Poišče opise vseh iger na spletni strani
	in jih shrani v seznam.
	"""
    mesto = 1
    for ujemanje in niz.finditer(stran):
        stevilo_ocen = int(ujemanje.group('stevilo_ocen').replace(',', ''))
        """Če je število ocen veliko, je podano z vejico, npr. 10,314."""
        
        if (int(ujemanje.group('leto')) <= meja_leto and 
            stevilo_ocen >= meja_ocene):
            """Zavrže najnovejše igre in igre s premalo ocenami."""
            video_igra = ujemanje.groupdict()
            video_igra['leto'] = int(video_igra['leto'])
            video_igra['odstotek'] = int(video_igra['odstotek'])
            video_igra['stevilo_ocen'] = stevilo_ocen
            video_igra['mesto'] = mesto
            mesto += 1
            ime_za_Python = ujemanje.group('ime').replace(' ', '_')
            slovar_iger[ime_za_Python] = video_igra
            
#            seznam_iger.append((ujemanje.group('ime'), 
#                                ujemanje.group('datum'), 
#                                int(ujemanje.group('leto')), 
#                                int(ujemanje.group('odstotek')), 
#                                stevilo_ocen,
#                                ujemanje.group('url')
#                                ))
    return slovar_iger

def stran_ene_igre(niz, stran, slovar_iger, ime_strani):
    """Poišče opis igre na njeni spletni strani
	in ga prečiščenega shrani v seznam.
	"""
    for ujemanje in niz.finditer(stran):
        stevilo_ocen = int(ujemanje.group('stevilo_ocen').replace(',', ''))
        """Če je število ocen veliko, je podano z vejico, npr. 10,314."""
        
        if (int(ujemanje.group('leto')) <= meja_leto and 
            stevilo_ocen >= meja_ocene):
            """Zavrže najnovejše igre in igre s premalo ocenami."""
            video_igra = ujemanje.groupdict()
            video_igra['leto'] = int(video_igra['leto'])
            video_igra['odstotek'] = int(video_igra['odstotek'])
            video_igra['stevilo_ocen'] = stevilo_ocen
            video_igra['mesto'] = mesto
            mesto += 1
            ime_za_Python = ujemanje.group('ime').replace(' ', '_')
            slovar_iger[ime_za_Python] = video_igra
            
#            seznam_iger.append((ujemanje.group('ime'), 
#                                ujemanje.group('datum'), 
#                                int(ujemanje.group('leto')), 
#                                int(ujemanje.group('odstotek')), 
#                                stevilo_ocen,
#                                ujemanje.group('url')
#                                ))
    return slovar_iger


meja_leto = 2016
meja_stevilo_ocen = 1000      

slovar_iger = {}
for ime_strani in os.listdir(pot):
    with open(os.path.join(pot, ime_strani), encoding="utf-8") as stran:
        vsebina_strani = stran.read()
    igre_stran(iskani_niz, vsebina_strani, slovar_iger=slovar_iger)


def nalozi_strani_iger(igre):
    os.makedirs('video_igre', exist_ok=True)
    for igra in igre:
        stran = requests.get(igre[igra]['url'])
        with open(os.path.join('video_igre', igra) + '.html', 'w', 
                  encoding='utf-8') as datoteka:
            datoteka.write(stran.text)

def preberi_strani_iger():
    for igra in slovar_iger:
        pot = os.path.join('video_igre', igra + '.html')
        with open(pot, encoding="utf-8") as stran:
            vsebina_strani = stran.read()
        stran_ene_igre(iskani_niz_2, vsebina_strani, slovar_iger=slovar_iger, ime_igre=igra)
    """ Regularni izraz, da prebere podatke. """

#nalozi_strani_iger(slovar_iger)
        
        
        
        
