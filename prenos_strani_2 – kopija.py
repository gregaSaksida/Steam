"""Prenese spletne strani s podrobnejsimi opisi iger."""

import requests
import os
import re

pot = 'spletne_strani'  #ime mape s spletnimi stranmi

def prenesi_stran(url, ime):
    """Funkcija prenese spletno stran in jo shrani pod danim imenom."""
    os.makedirs(pot, exist_ok=True)
    stran = requests.get(url)
    ime = ime + '.html'
    with open(os.path.join(pot, ime),
              'w', encoding='utf-8') as datoteka:
        datoteka.write(stran.text)
			

niz = re.compile(
	r'<div style="clear: left;"></div>.*?<a href="(?P<url>http.*?://store.steampowered.com/app/.*?topsellers_150_1)"  data-ds.*?'  #http.*? zaobjame http in https
	r'<span class="title">(?P<ime>.+?)</span>'
	r'.*?'
	r'row">(?P<datum>\d{1,2} [A-Z][a-z]{2}, (?P<leto>\d{4}))</div>'
	r'.*?'
	r'br&gt;(?P<odstotek>\d{1,2})% of the (?P<stevilo_ocen>(\d|,)*) user'  #delez dobrih ocen in stevilo vseh ocen
	r'.*?</span>',
	flags=re.DOTALL
)

slovar_iger = {}

"""Vseh zacetnih strani je 334, Python se zapelje cez vse.
for index in range(1, 335):
    datoteka = open(os.path.join(pot, 'stran_{}.html'.format(index)), 'r', 
                    encoding='utf-8')
    print(os.path.join(pot, 'stran_{}.html'.format(index)))  #Izpise, katero stran trenutno obdeluje.
    vsebina = datoteka.read()
    for ujemanje in niz.finditer(vsebina):
        stevilo_ocen = int(ujemanje.group('stevilo_ocen').replace(',', ''))
        ce je stevilo ocen veliko, je podano z vejico, npr. 10,314.
        if (int(ujemanje.group('leto')) <= 2017 and 
            stevilo_ocen >= 1000):
            Zavrze najnovejse igre in igre s premalo ocenami.
            slovar_iger[ujemanje.group('ime')] = ujemanje.group('url')
    datoteka.close() """
    
    
datoteka = open(os.path.join(pot, 'stran_1.html'), 'r', 
                encoding='utf-8')
print(1)  #Izpise, katero stran trenutno obdeluje.
vsebina = datoteka.read()
for ujemanje in niz.finditer(vsebina):
    print(ujemanje.group('ime'))
    print(ujemanje.group('url'))
    slovar_iger[ujemanje.group('ime')] = 1

datoteka2 = open(os.path.join(pot, 'stran_1.html'), 'r', 
                encoding='utf-8')
print(2)  #Izpise, katero stran trenutno obdeluje.
vsebina = datoteka2.read()
for ujemanje in niz.finditer(vsebina):
    stevilo_ocen = int(ujemanje.group('stevilo_ocen').replace(',', ''))
    """ce je stevilo ocen veliko, je podano z vejico, npr. 10,314."""
    slovar_iger[ujemanje.group('ime')] = ujemanje.group('url')

print(len(slovar_iger))

					
					