# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 12:44:59 2018

@author: Grega
"""

import os
import re
import json
import csv

pot = 'igre'


iskani_niz_1 = re.compile(
        r'<div class="user_reviews">.*?'
        r'<div class="subtitle column all">All Reviews:</div>.*?'
        r'- (?P<odstotek>\d{1,2})% of the (?P<stevilo_ocen>(\d|,){0,20}?) '
        r'user reviews for this game are positive.*?'  #ta in prejsnja vrstica: delez dobrih ocen in stevilo ocen
        r'<div class="release_date">.*?'
        r'<div class="subtitle column">Release Date:</div>.{0,20}?'
        r'<div class="date">(?P<datum>\d{1,2} [A-Z][a-z]{2}, (?P<leto>\d{4}))</div>'  #datum je oblike 12 Jan, 2016
        r'.*?<div class="subtitle column">Developer:</div>.{1,100}?developers_list".{1,400}?'
        r'">(?P<razvijalec>.{1,100}?)</a>'
        r'.*?<div class="subtitle column">Publisher:</div>.{1,100}summary column".{1,400}?'
        r'">(?P<izdajatelj>.{1,100}?)</a>'
        r'.*?<div class="glance_tags_label">Popular user-defined tags for this product:</div>.{1,400}? '
        r'style="display: none;">.{1,30}?'
        r'(?P<kategorije>\w.*?)\t{12}</a><div class="app_tag add_button"'
        r'.*?<b>Genre:</b>.*?">(?P<zanri>.*?)</a><br>'
        r'.*?<div class="game_purchase_price price">.{1,20}?'
        r'(?P<cena>Free to Play|\d{1,3},\d{1,2})'
        r'.*?System Requirements.*?Minimum:.*?Memory:</strong> (?P<RAM>\d{1,4} (K|M|G)B) RAM'
        r'.*?Storage:</strong> (?P<prostor>\d{1,4} (K|M|G)B) ',
        flags=re.DOTALL
)

"""Nekatere igre nimajo navedene minimalne zahteve za zmogljivost RAM-a in
prostora na disku. Pri njih uporabim drugi iskalni vzorec."""
iskani_niz_2 = re.compile(
        r'<div class="user_reviews">.*?'
        r'<div class="subtitle column all">All Reviews:</div>.*?'
        r'- (?P<odstotek>\d{1,2})% of the (?P<stevilo_ocen>(\d|,){0,20}?) '
        r'user reviews for this game are positive.*?'  #ta in prejsnja vrstica: delez dobrih ocen in stevilo ocen
        r'<div class="release_date">.*?'
        r'<div class="subtitle column">Release Date:</div>.{0,20}?'
        r'<div class="date">(?P<datum>\d{1,2} [A-Z][a-z]{2}, (?P<leto>\d{4}))</div>'  #datum je oblike 12 Jan, 2016
        r'.*?<div class="subtitle column">Developer:</div>.{1,100}?developers_list".{1,400}?'
        r'">(?P<razvijalec>.{1,100}?)</a>'
        r'.*?<div class="subtitle column">Publisher:</div>.{1,100}summary column".{1,400}?'
        r'">(?P<izdajatelj>.{1,100}?)</a>'
        r'.*?<div class="glance_tags_label">Popular user-defined tags for this product:</div>.{1,400}? '
        r'style="display: none;">.{1,30}?'
        r'(?P<kategorije>\w.*?)\t{12}</a><div class="app_tag add_button"'
        r'.*?<b>Genre:</b>.*?">(?P<zanri>.*?)</a><br>'
        r'.*?<div class="game_purchase_price price">.{1,20}?'
        r'(?P<cena>Free to Play|Free|\d{1,3},\d{1,2})',
        flags=re.DOTALL
)

seznam_iger = []
seznam_kategorij = []
seznam_zanrov = []
stevec = 1

"""Odpre stran z opisom igre"""
for igra in os.listdir(pot):
    datoteka = open(os.path.join(pot, igra), 'r', 
                    encoding='utf-8')
    vsebina = datoteka.read()
    
    """Poišče ujemanje, najprej poskusi strozjega."""
    niz_1 = False  # S to spremenljivko belezim, kateri od obeh nizov je bil najden.
    if iskani_niz_1.search(vsebina):
        ujemanje = iskani_niz_1.search(vsebina).groupdict()
        niz_1 = True
    elif iskani_niz_2.search(vsebina):
        ujemanje = iskani_niz_2.search(vsebina).groupdict()
    else:
        ujemanje = []
        
    """Skupina 'kategorije' in 'zanri' vsebuje tudi linke in odvecne znake. Z regularnimi
    izrazi jih nisem mogel izlociti, ker stevilo kategorij ni isto za vse igre."""
    if ujemanje:
        kategorije = ujemanje['kategorije']
        zanri = ujemanje['zanri']
        
        posebni_niz_1 = re.compile(
                r'\t{12}</a>'
                r'.*?'
                r'>..\t{12}',
                flags=re.DOTALL
                )
        """Zgornji regularni izraz opisuje niz, ki se pojavi med razlicnimi kategorijami."""
        while posebni_niz_1.search(kategorije):
            kategorije = re.sub(posebni_niz_1, ',', kategorije)
        ujemanje['kategorije'] = kategorije.split(',')
        for kategorija in ujemanje['kategorije']:
            seznam_kategorij.append({'ime': igra, 'kategorija': kategorija})
        
        posebni_niz_2 = re.compile(
                r'</a>, <a href=".*?">',
                flags=re.DOTALL
                )
        while posebni_niz_2.search(zanri):
            zanri = re.sub(posebni_niz_2, ',', zanri)
        ujemanje['zanri'] = zanri.split(',')
        for zanr in ujemanje['zanri']:
            seznam_zanrov.append({'ime': igra, 'zanr': zanr})
        
        ujemanje['ime'] = igra
        
        if ujemanje['cena'] == 'Free to Play' or ujemanje['cena'] == 'Free':
            ujemanje['cena'] = '0,0'
        else:
            cena = ujemanje['cena'].split(',')
            ujemanje['cena'] = int(cena[0]) + int(cena[1]) / 100
        
        """Pretvori zahteve za RAM in trdi disk v MB."""
        if niz_1:
            ram = ujemanje['RAM'].split()
            hd = ujemanje['prostor'].split()
            if ram[1] == 'GB':
                ujemanje['RAM'] = int(ram[0]) * 1024
            elif ram[1] == 'MB':
                ujemanje['RAM'] = int(ram[0])
            elif ram[1] == 'KB':
                ujemanje['RAM'] = int(ram[0]) / 1024
            if hd[1] == 'GB':
                ujemanje['prostor'] = int(hd[0]) * 1024
            elif hd[1] == 'MB':
                ujemanje['prostor'] = int(hd[0])
            elif hd[1] == 'KB':
                ujemanje['prostor'] = int(hd[0]) / 1024
        
        """Stevilo ocen pretvori iz zapisa z vejicami v navaden zapis."""
        stevilo_ocen = ujemanje['stevilo_ocen'].split(',')
        stevilo = 0
        faktor = len(stevilo_ocen) - 1
        for element in stevilo_ocen:
            stevilo += int(element) * (1000**faktor)
            faktor -= 1
        ujemanje['stevilo_ocen'] = stevilo
        
        seznam_iger.append(ujemanje)
    
    print(stevec)
    stevec += 1

with open('igre.json', 'w', encoding='utf-8') as datoteka:
    json.dump(seznam_iger, datoteka, indent=2)

def zapisi_csv(podatki, polja, ime_datoteke):
    with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
        pisalec = csv.DictWriter(datoteka, polja, extrasaction='ignore')
        pisalec.writeheader()
        for podatek in podatki:
            pisalec.writerow(podatek)

polja = ['ime', 'leto', 'odstotek', 'stevilo_ocen', 
         'cena', 'razvijalec', 'izdajatelj', 'RAM', 'prostor']
zapisi_csv(seznam_iger, polja, 'igre.csv')
zapisi_csv(seznam_kategorij, ['ime', 'kategorija'], 'kategorije.csv')
zapisi_csv(seznam_zanrov, ['ime', 'zanr'], 'zanri.csv')
        
        