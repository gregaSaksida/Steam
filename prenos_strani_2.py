"""Prenese spletne strani s podrobnejÅ¡imi opisi iger."""

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
			

iskani_niz = re.compile(
	r'.*?<a href="(?P<url>http.*?://store.steampowered.com/app/.*?)"  data-ds.*?'  #http.*? zaobjame http in https
	r'<span class="title">(?P<ime>.+?)</span>'
	r'.*?'
	r'row">(?P<datum>\d{1,2} [A-Z][a-z]{2}, (?P<leto>\d{4}))</div>'
	r'.*?'
	r'br&gt;(?P<odstotek>\d{1,2})% of the (?P<stevilo_ocen>(\d|,)*) user'  #deleÅ¾ dobrih ocen in Å¡tevilo vseh ocen
	r'.*?</span>',
	flags=re.DOTALL
)

def igre_stran(niz, stran, meja_leto=2017, meja_ocene=1000):
    """Na zaÄetni strani poiÅ¡Äe povezave do spletnih strani iger in jih prenese."""
    stevec = 1  #zgolj informativne narave
    for ujemanje in niz.finditer(vsebina):
        print(stevec)
        stevec += 1  #izpiše, katero podstran trenutno obdeluje
        stevilo_ocen = int(ujemanje.group('stevilo_ocen').replace(',', ''))
        """Äe je Å¡tevilo ocen veliko, je podano z vejico, npr. 10,314."""
        if (int(ujemanje.group('leto')) <= meja_leto and 
            stevilo_ocen >= meja_ocene):
            """ZavrÅ¾e najnovejÅ¡e igre ('meja_leto') in igre s premalo ocenami ('meja_ocene')."""
            prenesi_stran(ujemanje.group('url'), ujemanje.group('ime'))

"""Vseh zaÄetnih strani je 334, Python se zapelje Äez vse."""
for index in range(1, 335):
    datoteka = open(os.path.join(pot, 'stran_{}.html'.format(index)), 'r', 
                    encoding='utf-8')
    print(os.path.join(pot, 'stran_{}.html'.format(index)))  #IzpiÅ¡e, katero stran trenutno obdeluje.
    vsebina = datoteka.read()
    datoteka.close()
    igre_stran(iskani_niz, vsebina)
    #datoteka.close()

					
					