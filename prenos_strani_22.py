"""Prenese spletne strani s podrobnejsimi opisi iger."""

import requests
import os
import re

pot = 'spletne_strani'  #ime mape s spletnimi stranmi

def prenesi_stran(url, ime):
    """Funkcija prenese spletno stran in jo shrani pod danim imenom."""
    os.makedirs('igre', exist_ok=True)
    stran = requests.get(url, auth=('user', 'pass'))
    ime = ime + '.html'
    #print(os.path.join(pot, ime))
    with open(os.path.join('igre', ime),
              'w', encoding='utf-8') as datoteka:
        datoteka.write(stran.text)
			

iskani_niz = re.compile(
        r'(<div style="clear: left;"></div>|<!-- End Extra empty div -->).{0,50}?'
        r'<a href="(?P<url>http.{0,1}?://store.steampowered.com/'  #http.{0,1} zaobjame http in https
        r'(app|sub)/.{0,400}?)"  data-ds.{0,800}?'
        r'<span class="title">(?P<ime>.{1,100}?)</span>'
        r'.{0,700}?'
        r'row">(?P<datum>\d{1,2} [A-Z][a-z]{2}, (?P<leto>\d{4}))</div>'  #datum je oblike 12 Jan, 2016
        r'.{100,300}?'
        r'br&gt;(?P<odstotek>\d{1,2})% of the (?P<stevilo_ocen>(\d|,){0,20}?) user reviews for this game',  #delez dobrih ocen in stevilo vseh ocen
	flags=re.DOTALL
)
"""Na vsaki strani pricakujem 15-20 zadetkov. Če uporabim zgolj .*?, namesto da
navedem tocno stevilo znakov, lahko vec iger prepozna kot en zadetek
(nekatere igre recimo nimajo zapisanega stevila ocen)."""


slovar_iger = {}

"""Vseh zacetnih strani je 334, Python se zapelje cez vse."""
for index in range(1, 335):
    datoteka = open(os.path.join(pot, 'stran_{}.html'.format(index)), 'r', 
                    encoding='utf-8')
    #print(os.path.join(pot, 'stran_{}.html'.format(index)))  #Izpise, katero stran trenutno obdeluje.
    vsebina = datoteka.read()
    for ujemanje in iskani_niz.finditer(vsebina):
        stevilo_ocen = int(ujemanje.group('stevilo_ocen').replace(',', ''))
        """ce je stevilo ocen veliko, je podano z vejico, npr. 10,314."""
        if (int(ujemanje.group('leto')) <= 2017 and 
            stevilo_ocen >= 1000):
            """Zavrze najnovejse igre in igre s premalo ocenami."""
            ime = ujemanje.group('ime').replace('/',',').replace(':',',').replace('*',',').replace('?',',').replace('<',',').replace('>',',').replace('"',',').replace('\\',',')  #Windows teh znakov v imenu datotek ne dopusti.
            slovar_iger[ime] = ujemanje.group('url')
    datoteka.close()

stevec = 1
print('Program bo sedaj prenesel {} spletnih strani.'.format(len(slovar_iger)))

for ime in slovar_iger:
    prenesi_stran(slovar_iger[ime], ime)
    print(stevec)
    stevec += 1